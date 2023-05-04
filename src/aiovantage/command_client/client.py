import asyncio
import logging
import ssl
from collections import defaultdict
from inspect import iscoroutinefunction
from itertools import islice
from types import TracebackType
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

from .errors import CommandExecutionError, LoginFailedError, LoginRequiredError
from .events import Event, EventType
from .helpers import tokenize_response


# Type alias for connections
Connection = Tuple[asyncio.StreamReader, asyncio.StreamWriter]

# Types for callbacks for event subscriptions
EventCallback = Callable[[Event], None]
EventSubscription = Tuple[EventCallback, Optional[Iterable[EventType]]]


class CommandClient:
    """
    Communicate with the Vantage InFusion "Host Command" service.

    The Host Command service is a TCP text-based service that allows interaction with
    devices controlled by a Vantage InFusion Controller.

    Among other things, this service allows you to query and change the state of devices
    attached to a Vantage system (eg. turn on/off a light) as well as subscribe to
    status changes for devices.

    The service is exposed on port 3010 (SSL) by default, and on port 3001 (non-SSL) if
    this port has been opened by the firewall on the controller.
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        use_ssl: bool = True,
        port: Optional[int] = None,
        conn_timeout: float = 5,
        read_timeout: float = 5,
        max_connection_attempts: Optional[int] = None,
        backoff_fn: Callable[[int], float] = lambda n: 5,
    ) -> None:
        """
        Initialize the HCClient instance.

        Args:
            host: The hostname or IP address of the Host Command service.
            username: The username to use to authenticate.
            password: The password to use to authenticate.
            use_ssl: Whether to use SSL when connecting.
            port: The port to use when connecting.
            conn_timeout: The timeout to use when connecting.
            read_timeout: The timeout to use when reading.
            max_retries: The maximum number of times to attempt to reconnect.
            backoff_fn: A function that takes the number of retries and returns the
                        number of seconds to wait before retrying.
        """

        self._host = host
        self._username = username
        self._password = password
        self._ssl_context = None
        self._logger = logging.getLogger(__name__)
        self._connection: Optional[Connection] = None
        self._conn_lock = asyncio.Lock()
        self._request_lock = asyncio.Lock()
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._tasks: List[asyncio.Task[None]] = []
        self._max_connection_attempts: Optional[int] = max_connection_attempts
        self._backoff_fn = backoff_fn
        self._previously_connected = False
        self._response_queue: asyncio.Queue[str] = asyncio.Queue()
        self._status_queue: asyncio.Queue[str] = asyncio.Queue()
        self._event_log_queue: asyncio.Queue[str] = asyncio.Queue()
        self._subscriptions: List[EventSubscription] = []
        self._event_log_subscribed_types: Dict[str, int] = defaultdict(int)

        # Set up SSL context
        if use_ssl is True:
            # We don't have a local issuer certificate to check against, and we'll be
            # connecting to an IP address so we can't check the hostname
            self._ssl_context = ssl.create_default_context()
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE
        elif isinstance(use_ssl, ssl.SSLContext):
            self._ssl_context = use_ssl

        # Set up port
        if port is None:
            self._port = 3010 if use_ssl else 3001
        else:
            self._port = port

    async def __aenter__(self) -> "CommandClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the connection to the service and cancel any running tasks."""

        # Cancel any running tasks
        for task in self._tasks:
            task.cancel()
        self._tasks = []

        # Check if connection is already closed
        if self._connection is None or self._connection[1].is_closing():
            return

        # Close the connection
        _, writer = self._connection
        writer.close()
        await writer.wait_closed()

        self._logger.debug("Connection closed")

    async def raw_request(self, request: str) -> List[str]:
        """
        Send a raw string request to the Host Command service, returning all lines of
        the response, until the "R:" line is received.

        Args:
            request: The request string to send.

        Returns:
            A list of response lines.
        """

        # Get the connection
        _, writer = await self._get_connection()

        # Send the request
        async with self._request_lock:
            self._logger.debug(f"Sending request: {request}")
            writer.write(f"{request}\n".encode())
            await writer.drain()

            # Grab every line of the response, until we get a "R:" return line
            response = []
            while True:
                # Wait for a response line
                line = await asyncio.wait_for(
                    self._response_queue.get(), self._read_timeout
                )
                self._response_queue.task_done()

                # Add the line to the response
                response.append(line)
                if line.startswith("R:"):
                    break

            return response

    async def command(self, command: str, *params: Union[int, float, str]) -> List[str]:
        """
        Send a command with parameters to the Host Command service, and return the
        arguments of the "R:" line of the response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command, int, float, or str.

        Returns:
            A list of response arguments.
        """

        if not all(isinstance(param, (int, float, str)) for param in params):
            raise TypeError("Command parameters must be int, float, or str")

        # Build the request string, encoding the parameters if necessary
        if params:
            request = f"{command} {' '.join([str(p) for p in params])}"
        else:
            request = command

        # Send the request
        response_lines = await self.raw_request(request)

        # Get the "R:" return line and split it into parts
        response = response_lines[-1]
        reply, *args = tokenize_response(response)

        # Check for errors
        if reply.startswith("R:ERROR"):
            _, _, error_code_str = reply.split(":")
            error_code = int(error_code_str)
            error_message = args[0]
            if error_code == 21:
                raise LoginRequiredError(error_message)
            elif error_code == 23:
                raise LoginFailedError(error_message)
            else:
                raise CommandExecutionError(
                    f"{error_message} (Error code {error_code})"
                )

        # Check for out of order responses
        if not reply == f"R:{command.upper()}":
            raise Exception(
                f"Received out of order response."
                f"\tExpected: {command}"
                f"\tReceived: {response}"
            )

        return args

    async def invoke(
        self, id: int, method: str, *params: Union[int, float, str]
    ) -> List[str]:
        """
        Send an INVOKE command to invoke a method on an Vantage object.

        Args:
            id: The id of the object to invoke the method on.
            method: The name of the method to invoke.
            params: The parameters to pass to the method.

        Returns:
            A list of response arguments.
        """

        return await self.command("INVOKE", id, method, *params)

    async def login(self, username: str, password: str) -> None:
        """
        Send a LOGIN command to authenticate with the Host Command service.

        Args:
            username: The username to authenticate with.
            password: The password to authenticate with.
        """

        await self.command("LOGIN", username, password)

        self._logger.info("Logged in")

    async def addstatus(self, ids: Union[int, Iterable[int]]) -> None:
        """
        Send an ADDSTATUS command to subscribe to status events for the given ids.

        Args:
            ids: The ids to subscribe to status events for.
        """

        if isinstance(ids, int):
            ids = (ids,)

        # ADDSTATUS accepts up to 16 ids at a time, so chunk the requests.
        id_iter = iter(ids)
        while id_chunk := tuple(islice(id_iter, 16)):
            await self.command("ADDSTATUS", *id_chunk)

    async def delstatus(self, ids: Union[int, Iterable[int]]) -> None:
        """
        Send a DELSTATUS command to unsubscribe from status events for the given ids.

        Args:
            ids: The ids to unsubscribe from status events for.
        """

        if isinstance(ids, int):
            ids = (ids,)

        # DELSTATUS accepts up to 16 ids at a time, so chunk the requests.
        id_iter = iter(ids)
        while id_chunk := tuple(islice(id_iter, 16)):
            await self.command("DELSTATUS", *id_chunk)

    def subscribe(
        self,
        callback: EventCallback,
        event_filter: Union[EventType, Iterable[EventType], None],
    ) -> Callable[[], None]:
        """
        Subscribe to Host Command events, optionally filtering by event type.

        Args:
            callback: The callback to call when an event is received.
            event_filter: The event type(s) to filter by, or None to receive all events.

        Returns:
            A callback that can be called to unsubscribe.
        """

        # Convert the event_filter to a tuple if it's a single EventType
        if isinstance(event_filter, EventType):
            event_filter = (event_filter,)

        # Add the subscription
        subscription = (callback, event_filter)
        self._subscriptions.append(subscription)

        # Return the unsubscribe callback
        def unsubscribe() -> None:
            # Remove the subscription
            self._subscriptions.remove(subscription)

        return unsubscribe

    async def subscribe_status(
        self,
        callback: EventCallback,
        status_types: Union[str, Iterable[str]],
    ) -> Callable[[], Awaitable[None]]:
        """
        Subscribe to status events for the given status types, using "STATUS {type}".

        Args:
            callback: The callback to call when a status event is received.
            status_types: The status types to subscribe to status events for.

        Returns:
            A coroutine to unsubscribe from status events.
        """

        if isinstance(status_types, str):
            status_types = (status_types,)

        # Filter recived status events by type
        def filtered_callback(event: Event) -> None:
            if event["tag"] != EventType.STATUS:
                return

            # Apply the status type filter
            if event["status_type"] not in status_types:
                return

            callback(event)

        # Add the subscription to the list
        remove_subscription = self.subscribe(filtered_callback, EventType.STATUS)

        # Ask the controller to start sending status events
        for status_type in status_types:
            await self.command("STATUS", status_type)

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            remove_subscription()

        return unsubscribe

    async def subscribe_objects(
        self,
        callback: EventCallback,
        object_ids: Union[int, Iterable[int]],
    ) -> Callable[[], Awaitable[None]]:
        """
        Subscribe to status events for the given object ids, using "ADDSTATUS {id}".

        Args:
            callback: The callback to call when a status event is received.
            object_ids: The ids to subscribe to status events for.

        Returns:
            A coroutine to unsubscribe from status events.
        """

        if isinstance(object_ids, int):
            object_ids = (object_ids,)

        # Filter recived status events by id
        def filtered_callback(event: Event) -> None:
            if event["tag"] != EventType.STATUS:
                return

            # Apply the object id filter
            if event["id"] not in object_ids:  # type: ignore[operator]
                return

            callback(event)

        # Add the subscription to the list
        remove_subscription = self.subscribe(filtered_callback, EventType.STATUS)

        # Ask the controller to start sending status events for these objects
        await self.addstatus(object_ids)

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            await self.delstatus(object_ids)
            remove_subscription()

        return unsubscribe

    async def subscribe_event_log(
        self,
        callback: EventCallback,
        log_types: Union[str, Iterable[str]],
    ) -> Callable[[], Awaitable[None]]:
        """
        Subscribe to event log events, using "ELLOG {type} ON".

        Args:
            callback: The callback to call when an event log event is received.
            log_types: The event log types to subscribe to.

        Returns:
            A coroutine to unsubscribe from event log events.
        """

        if isinstance(log_types, str):
            log_types = (log_types,)

        # Add the subscription to the list
        remove_subscription = self.subscribe(callback, EventType.EVENT_LOG)

        # Ask the controller to start sending event logs for these types
        for log_type in log_types:
            if self._event_log_subscribed_types[log_type] == 0:
                await self.command("ELENABLE", log_type, "ON")
                await self.command("ELLOG", log_type, "ON")

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            for log_type in log_types:
                self._event_log_subscribed_types[log_type] -= 1

                if self._event_log_subscribed_types[log_type] == 0:
                    await self.command("ELLOG", log_type, "OFF")

            remove_subscription()

        return unsubscribe

    async def _get_connection(self) -> Connection:
        # Get a connection to the controller, reconnecting if necessary

        async with self._conn_lock:
            # If we already have a connection, return it
            if self._connection is not None and not self._connection[1].is_closing():
                return self._connection

            # Otherwise, try to establish a new connection, retrying if necessary
            attempts = 0
            while True:
                try:
                    # Otherwise, open a new connection
                    self._connection = await asyncio.wait_for(
                        asyncio.open_connection(
                            self._host,
                            self._port,
                            ssl=self._ssl_context,
                        ),
                        timeout=self._conn_timeout,
                    )

                    break
                except (ConnectionError, OSError, asyncio.TimeoutError):
                    # Retry with backoff if the connection fails
                    attempts += 1
                    if (
                        self._max_connection_attempts is not None
                        and attempts >= self._max_connection_attempts
                    ):
                        raise

                    delay = self._backoff_fn(attempts)
                    self._logger.warning(
                        f"Connection to {self._host}:{self._port} failed, "
                        f"retrying in {delay} seconds"
                    )
                    await asyncio.sleep(delay)

            # Login if we have a username and password
            if self._username and self._password:
                await self.login(self._username, self._password)

            # Notify subscribers that we've connected
            if self._previously_connected:
                self._emit({"tag": EventType.RECONNECTED})
            else:
                self._emit({"tag": EventType.CONNECTED})
                self._previously_connected = True

            # Start tasks to handle incoming messages
            self._tasks.append(asyncio.create_task(self._handle_messages()))
            self._tasks.append(asyncio.create_task(self._status_processor()))
            self._tasks.append(asyncio.create_task(self._event_log_processor()))

            self._logger.info("Connected and listening for messages")

            return self._connection

    def _emit(self, event: Event) -> None:
        # Emit an event to all subscribers.

        for callback, event_types in self._subscriptions:
            if event_types is None or event["tag"] in event_types:
                if iscoroutinefunction(callback):
                    asyncio.create_task(callback(event))
                else:
                    callback(event)

    async def _handle_messages(self) -> None:
        # Fetch new messages from the reader and enqueue them for processing

        reader, _ = await self._get_connection()
        while True:
            try:
                data = await reader.readline()
            except ConnectionError:
                self._logger.warning("Connection lost in _handle_messages")
                break

            if not data:
                self._logger.warning("EOF in _handle_messages")
                break

            message = data.decode().rstrip()
            self._logger.debug(f"Received message: {message}")

            if message.startswith("S:"):
                self._status_queue.put_nowait(message)
            elif message.startswith("EL:"):
                self._event_log_queue.put_nowait(message)
            else:
                self._response_queue.put_nowait(message)

        # If we get here, the connection was closed
        self._emit({"tag": EventType.DISCONNECTED})

        # Try to reconnect
        async def reconnect() -> None:
            await self.close()
            await self._get_connection()

        asyncio.create_task(reconnect())

    async def _event_log_processor(self) -> None:
        # Process event log messages from the queue and dispatch to subscribers

        while True:
            try:
                # Grab the next event log message from the queue
                message = await self._event_log_queue.get()
                message = message[4:]
                self._event_log_queue.task_done()

                # Notify subscribers
                self._emit({"tag": EventType.EVENT_LOG, "log": message})
            except Exception:
                self._logger.exception(f"Error processing event log message: {message}")

    async def _status_processor(self) -> None:
        # Process status messages from the queue and dispatch to subscribers

        while True:
            try:
                # Grab the next status message from the queue
                message = await self._status_queue.get()
                self._status_queue.task_done()

                # Parse the status message
                status_type, id_str, *args = tokenize_response(message)
                status_type = status_type[2:]
                id = int(id_str)

                # Notify subscribers
                self._emit(
                    {
                        "tag": EventType.STATUS,
                        "status_type": status_type,
                        "id": id,
                        "args": args,
                    },
                )
            except Exception:
                self._logger.exception(f"Error processing status message: {message}")
