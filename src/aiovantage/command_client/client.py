import asyncio
import logging
import ssl
from collections import defaultdict
from inspect import iscoroutinefunction
from types import TracebackType
from typing import (
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

from .errors import (
    CommandExecutionError,
    LoginFailedError,
    LoginRequiredError,
    NotConnectedError,
)
from .events import Event, EventType
from .helpers import tokenize_response


# Type alias for connections
Connection = Tuple[asyncio.StreamReader, asyncio.StreamWriter]

# Type aliases for callbacks for event subscriptions
EventCallback = Callable[[Event], None]
EventSubscription = Tuple[EventCallback, Optional[Iterable[EventType]]]


def create_ssl_context() -> ssl.SSLContext:
    """
    Creates a default SSL context that doesn't verify hostname or certificate.

    We don't have a local issuer certificate to check against, and we'll most likely be
    connecting to an IP address, so we can't check the hostname.
    """

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


class CommandProtocol(asyncio.Protocol):
    """
    Async I/O Protocol implementation for the Vantage Host Command service that handles
    buffering and parsing of messages, and provides queues for command responses and
    "events" such as "status" events, and "event log" events.
    """

    def __init__(self) -> None:
        self._transport: Optional[asyncio.Transport] = None
        self._buffer = bytearray()
        self._response_buffer: List[str] = []
        self._response_queue: asyncio.Queue[List[str]] = asyncio.Queue()
        self._event_queue: asyncio.Queue[Union[str, Exception]] = asyncio.Queue()
        self._delimiter = b"\r\n"

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self._transport = cast(asyncio.Transport, transport)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc is not None:
            self._event_queue.put_nowait(exc)

        self._transport = None

    def data_received(self, data: bytes) -> None:
        # Add the new data to the buffer
        self._buffer.extend(data)

        # Check for newlines in the buffer and process any complete lines
        while self._delimiter in self._buffer:
            line, self._buffer = self._buffer.split(self._delimiter, 1)
            message = line.decode()
            if message.startswith("R:"):
                self._response_buffer.append(message)
                self._response_queue.put_nowait(self._response_buffer.copy())
                self._response_buffer = []
            elif message.startswith("S:") or message.startswith("EL:"):
                self._event_queue.put_nowait(message)
            else:
                self._response_buffer.append(message)

    def eof_received(self) -> Optional[bool]:
        self._event_queue.put_nowait(EOFError("EOF received"))
        return False

    def is_connected(self) -> bool:
        return self._transport is not None and not self._transport.is_closing()

    def close(self) -> None:
        if self._transport is not None:
            self._transport.close()
            self._transport = None

    @property
    def response_queue(self) -> asyncio.Queue[List[str]]:
        return self._response_queue

    @property
    def event_queue(self) -> asyncio.Queue[Union[str, Exception]]:
        return self._event_queue


class CommandConnection:
    """
    A connection to the Vantage Host Command service that handles sending
    commands and receiving responses and events.
    """

    def __init__(
        self,
        host: str,
        port: int,
        *,
        ssl: Optional[ssl.SSLContext] = None,
        conn_timeout: Optional[float] = 5,
        read_timeout: Optional[float] = 10,
    ) -> None:
        self._host = host
        self._port = port
        self._ssl = ssl
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._protocol: Optional[CommandProtocol] = None
        self._lock: asyncio.Lock = asyncio.Lock()

    async def __aenter__(self) -> "CommandConnection":
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    @property
    def transport(self) -> Optional[asyncio.Transport]:
        if self._protocol is None:
            return None

        return self._protocol._transport

    @property
    def protocol(self) -> Optional[CommandProtocol]:
        return self._protocol

    async def open(self) -> None:
        """Open a connection to the Vantage Host Command service."""

        # If we're already connected, do nothing
        if self.protocol is not None and self.protocol.is_connected():
            return

        # Create the connection using our protocol
        loop = asyncio.get_running_loop()
        _, self._protocol = await asyncio.wait_for(
            loop.create_connection(
                CommandProtocol, self._host, self._port, ssl=self._ssl
            ),
            timeout=self._conn_timeout,
        )

    def close(self) -> None:
        """Close the connection to the Vantage Host Command service."""

        if self.protocol is not None:
            self.protocol.close()

    async def raw_request(self, request: str) -> List[str]:
        """
        Send a raw string request to the Vantage Host Command service, returning all
        lines of the response, until the "R:" line is received.

        Args:
            request: The request string to send.

        Returns:
            A list of response lines.
        """

        async with self._lock:
            # Make sure we're connected
            if self.protocol is None or not self.protocol.is_connected():
                raise NotConnectedError("Not connected to Vantage Host Command service")

            # Send the request
            self.transport.write(f"{request}\n".encode())  # type: ignore[union-attr]

            # Wait for the response
            return await asyncio.wait_for(
                self.protocol.response_queue.get(), timeout=self._read_timeout
            )

    async def command(self, command: str, *params: Union[int, float, str]) -> List[str]:
        """
        Send a command with parameters to the Vantage Host Command service, and return
        the arguments of the "R:" line of the response.

        Handles encoding parameters, and raises an exception if the response was an
        error response (R:ERROR).

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command, int, float, or str.

        Returns:
            A list of response arguments.
        """

        # Validate parameters
        if not all(isinstance(param, (int, float, str)) for param in params):
            raise TypeError("Command parameters must be int, float, or str")

        # Build the request string, encoding the parameters if necessary
        if params:
            request = f"{command} {' '.join([str(p) for p in params])}"
        else:
            request = command

        # Send the request
        response = await self.raw_request(request)

        # Get the "R:" return line and split it into parts
        reply, *args = tokenize_response(response[-1])

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

    async def events(self) -> AsyncIterator[str]:
        """
        An async iterator that yields events from the Host Command service.

        Yields:
            "S:" (Status) or "EL:" (Event Log) strings from the Host Command service.
        """

        # Make sure we're connected
        if self.protocol is None or not self.protocol.is_connected():
            raise NotConnectedError("Not connected to Vantage Host Command service")

        # Yield events from the event queue
        while True:
            result = await self.protocol.event_queue.get()
            if isinstance(result, Exception):
                raise result

            yield result


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
        conn_timeout: Optional[float] = 5,
        read_timeout: Optional[float] = 10,
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
        """

        self._host = host
        self._username = username
        self._password = password
        self._ssl_context = None
        self._logger = logging.getLogger(__name__)
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._event_handler_connected: asyncio.Event = asyncio.Event()
        self._event_handler_connection: Optional[CommandConnection] = None
        self._event_handler_task: Optional[asyncio.Task[None]] = None
        self._subscriptions: List[EventSubscription] = []
        self._subscribed_statuses: Dict[str, int] = defaultdict(int)
        self._subscribed_objects: Dict[int, int] = defaultdict(int)
        self._subscribed_event_logs: Dict[str, int] = defaultdict(int)

        # Set up SSL context
        if use_ssl is True:
            self._ssl_context = create_ssl_context()
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
        """
        Close the connection to the Host Command service and stop the event handler.
        """

        # Stop the event handler
        if self._event_handler_task is not None:
            self._event_handler_task.cancel()
            try:
                await self._event_handler_task
            except asyncio.CancelledError:
                pass
            self._event_handler_task = None

        # Close the connection
        if self._event_handler_connection is not None:
            self._event_handler_connection.close()
            self._event_handler_connection = None

    async def command(self, command: str, *params: Union[int, float, str]) -> List[str]:
        """
        Send a command with parameters to the Host Command service, and return the
        arguments of the "R:" line of the response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command, int, float, or str.
            connection: The connection to use, or None to get a new connection.

        Returns:
            A list of response arguments.
        """

        conn = await self._create_connection()
        response = await conn.command(command, *params)
        conn.close()

        return response

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

        # Support passing a single EventType
        if isinstance(event_filter, EventType):
            event_filter = (event_filter,)

        # Add the subscription
        subscription = (callback, event_filter)
        self._subscriptions.append(subscription)

        # Return an unsubscribe callback to remove the subscription
        def unsubscribe() -> None:
            self._subscriptions.remove(subscription)

        return unsubscribe

    async def subscribe_status(
        self, callback: EventCallback, status_types: Union[str, Iterable[str]]
    ) -> Callable[[], Awaitable[None]]:
        """
        Subscribe to status events for the given status types, using "STATUS {type}".

        Args:
            callback: The callback to call when a status event is received.
            status_types: The status types to subscribe to status events for.

        Returns:
            A coroutine to unsubscribe from status events.
        """

        # Support passing a single status type
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

        # Ask the Host Command service to start sending status events
        conn = await self._get_event_handler_connection()
        for status_type in status_types:
            self._subscribed_statuses[status_type] += 1
            if self._subscribed_statuses[status_type] == 1:
                await conn.command("STATUS", status_type)

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            for status_type in status_types:
                self._subscribed_statuses[status_type] -= 1

            remove_subscription()

        return unsubscribe

    async def subscribe_objects(
        self, callback: EventCallback, object_ids: Union[int, Iterable[int]]
    ) -> Callable[[], Awaitable[None]]:
        """
        Subscribe to status events for the given object ids, using "ADDSTATUS {id}".

        Args:
            callback: The callback to call when a status event is received.
            object_ids: The ids to subscribe to status events for.

        Returns:
            A coroutine to unsubscribe from status events.
        """

        # Support passing a single object id
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

        # Get the event handler connection
        conn = await self._get_event_handler_connection()

        # Ask the controller to start sending status events for these objects
        for object_id in object_ids:
            self._subscribed_objects[object_id] += 1
            if self._subscribed_objects[object_id] == 1:
                await conn.command("ADDSTATUS", object_id)

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            for object_id in object_ids:  # type: ignore[union-attr]
                self._subscribed_objects[object_id] -= 1
                if self._subscribed_objects[object_id] == 0:
                    await conn.command("DELSTATUS", object_id)

            remove_subscription()

        return unsubscribe

    async def subscribe_event_log(
        self, callback: EventCallback, log_types: Union[str, Iterable[str]]
    ) -> Callable[[], Awaitable[None]]:
        """
        Subscribe to event log events, using "ELLOG {type} ON".

        Args:
            callback: The callback to call when an event log event is received.
            log_types: The event log types to subscribe to.

        Returns:
            A coroutine to unsubscribe from event log events.
        """

        # Support passing a single log type
        if isinstance(log_types, str):
            log_types = (log_types,)

        # Add the subscription to the list
        remove_subscription = self.subscribe(callback, EventType.EVENT_LOG)

        # Get the event handler connection
        conn = await self._get_event_handler_connection()

        # Ask the controller to start sending event logs for these types
        for log_type in log_types:
            self._subscribed_event_logs[log_type] += 1
            if self._subscribed_event_logs[log_type] == 1:
                await conn.command("ELENABLE", log_type, "ON")
                await conn.command("ELLOG", log_type, "ON")

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            for log_type in log_types:
                self._subscribed_event_logs[log_type] -= 1
                if self._subscribed_event_logs[log_type] == 0:
                    await conn.command("ELLOG", log_type, "OFF")

            remove_subscription()

        return unsubscribe

    def emit(self, event: Event) -> None:
        """Emit an event to all subscribers."""

        for callback, event_types in self._subscriptions:
            if event_types is None or event["tag"] in event_types:
                if iscoroutinefunction(callback):
                    asyncio.create_task(callback(event))
                else:
                    callback(event)

    async def _get_event_handler_connection(self) -> CommandConnection:
        # Get the event handler connection, starting the task if necessary

        await self._start_event_handler()
        assert self._event_handler_connection is not None
        return self._event_handler_connection

    async def _start_event_handler(self) -> None:
        # Start the event handler if it's not already running

        # Return if the event handler is already running
        if self._event_handler_task is not None:
            return

        # Otherwise, start the event handler task
        self._event_handler_task = asyncio.create_task(self._event_handler())

        # Wait for the event handler to connect before returning
        await self._event_handler_connected.wait()

    async def _create_connection(self) -> CommandConnection:
        # Get a new connection to the Host Command service, authenticating if necessary

        conn = CommandConnection(self._host, self._port, ssl=self._ssl_context)
        await conn.open()

        # Log in if we have credentials
        if self._username is not None and self._password is not None:
            await conn.command("LOGIN", self._username, self._password)

        return conn

    async def _resubscribe(self, conn: CommandConnection) -> None:
        # Re-subscribe to events after a reconnection

        # Re-subscribe to status events
        for status_type, count in self._subscribed_statuses.items():
            if count > 0:
                await conn.command("STATUS", status_type)

        # Re-subscribe to object events
        for object_id, count in self._subscribed_objects.items():
            if count > 0:
                await conn.command("ADDSTATUS", object_id)

        # Re-subscribe to event log events
        for log_type, count in self._subscribed_event_logs.items():
            if count > 0:
                await conn.command("ELENABLE", log_type, "ON")
                await conn.command("ELLOG", log_type, "ON")

    async def _event_handler(self) -> None:
        # The event handler task

        connect_attempts = 0
        while True:
            connect_attempts += 1
            try:
                # Get a connection
                conn = await self._create_connection()
                self._event_handler_connection = conn
                self._logger.info("Connected and listening for events")

                # Signal that we're connected
                if self._event_handler_connected.is_set():
                    await self._resubscribe(conn)
                    self.emit({"tag": EventType.RECONNECTED})

                else:
                    self._event_handler_connected.set()
                    self.emit({"tag": EventType.CONNECTED})

                # Start processing events
                async for event in conn.events():
                    self._logger.debug(f"Received event: {event}")

                    if event.startswith("S:"):
                        # Parse a status message
                        status_type, id_str, *args = tokenize_response(event)
                        status_type = status_type[2:]
                        id = int(id_str)

                        # Notify subscribers
                        self.emit(
                            {
                                "tag": EventType.STATUS,
                                "status_type": status_type,
                                "id": id,
                                "args": args,
                            },
                        )
                    elif event.startswith("EL:"):
                        # Parse an event log message
                        message = event[4:]
                        self.emit({"tag": EventType.EVENT_LOG, "log": message})

            except (ConnectionError, OSError, EOFError, asyncio.TimeoutError):
                # Connection error either during the connection attempt or while
                # processing events
                print("Connection error in _event_handler")
            except Exception:
                self._logger.exception("Unknown error in _event_handler")

            self.emit({"tag": EventType.DISCONNECTED})

            print("Retrying in 5 seconds")
            await asyncio.sleep(5)
