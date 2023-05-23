import asyncio
import logging
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass
from inspect import iscoroutinefunction
from ssl import SSLContext, SSLError
from types import TracebackType
from typing import (
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

from .errors import NotConnectedError, command_error_from_string
from .events import Event, EventType
from .helpers import tokenize_response
from .ssl import create_ssl_context


# Type alias for connections
Connection = Tuple[asyncio.StreamReader, asyncio.StreamWriter]

# Type aliases for callbacks for event subscriptions
EventCallback = Union[Callable[[Event], None], Callable[[Event], Awaitable[None]]]
EventSubscription = Tuple[EventCallback, Optional[Iterable[EventType]]]


@dataclass
class CommandResponse:
    """
    Simple wrapper for command responses from the Vantage Host Command service.
    """

    command: str
    """The command that was sent."""

    args: List[str]
    """The arguments of the "R:" line of the response."""

    data: List[str]
    """The data lines of the response, before the "R:" line."""

    def __init__(self, data: List[str]) -> None:
        # Extract "data" lines from the response. These are any lines before the
        # "R:" line, from commands such as "HELP" and "LISTSTATUS".
        self.data, return_line = data[:-1], data[-1]

        # Split the "R:" line into the command and arguments
        command, *self.args = tokenize_response(return_line)

        # Remove the "R:" prefix from the command
        self.command = command[2:]


class HostCommandConnection:
    """
    A connection to the Vantage Host Command service that handles sending
    commands and receiving responses and events.
    """

    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        *,
        ssl: Union[SSLContext, bool, None] = None,
        conn_timeout: Optional[float] = 5,
        read_timeout: Optional[float] = 10,
    ) -> None:
        """
        Create a connection to the Vantage Host Command service.

        Args:
            host: The hostname or IP address of the Vantage host.
            port: The port to connect to. Defaults to 3010 if SSL is enabled, else 3001.
            ssl: Whether to use SSL for the connection. If True, a default SSL context
                will be created. If False, SSL will not be used. If a SSLContext is
                provided, it will be used.
            conn_timeout: The timeout for establishing a connection, in seconds.
            read_timeout: The timeout for reading a response, in seconds.
        """

        self._host = host
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None

        self._delimiter = b"\r\n"
        self._command_lock: asyncio.Lock = asyncio.Lock()
        self._response_buffer: List[str] = []
        self._response_queue: asyncio.Queue[
            Union[CommandResponse, Exception]
        ] = asyncio.Queue(1)
        self._event_queues: Set[asyncio.Queue[Union[str, Exception]]] = set()
        self._task: Optional[asyncio.Task[None]] = None
        self._logger = logging.getLogger(__name__)

        # Set up the SSL context
        self._ssl: Optional[SSLContext]
        if ssl is True:
            self._ssl = create_ssl_context()
        elif isinstance(ssl, SSLContext):
            self._ssl = ssl
        else:
            self._ssl = None

        # Set up the port
        self._port: int
        if port is None:
            self._port = 3010 if ssl else 3001
        else:
            self._port = port

    async def __aenter__(self) -> "HostCommandConnection":
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    async def open(self) -> None:
        """Open a connection to the Vantage Host Command service."""

        # If we're already connected, do nothing
        if self._writer is not None and not self._writer.is_closing():
            return

        # Create the connection
        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(self._host, self._port, ssl=self._ssl),
            timeout=self._conn_timeout,
        )

        # Start the message handler task
        self._task = asyncio.create_task(self._message_handler())

    def close(self) -> None:
        """Close the connection to the Vantage Host Command service."""

        # Cancel the message handler task
        if self._task is not None:
            self._task.cancel()
            self._task = None

        # Close the underlying connection
        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()
            self._writer = None

    @property
    def closed(self) -> bool:
        """Whether the connection is closed."""

        return self._writer is None or self._writer.is_closing()

    async def command(
        self, command: str, *params: Union[int, float, str]
    ) -> CommandResponse:
        """
        Send a command with parameters to the Host Command service and wait for a
        response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command, int, float, or str.

        Returns:
            A CommandResponse instance.
        """

        # Make sure we're connected
        if self._writer is None or self._writer.is_closing():
            raise NotConnectedError("Not connected to Vantage Host Command service")

        # Validate parameters
        if not all(isinstance(param, (int, float, str)) for param in params):
            raise TypeError("Command parameters must be int, float, or str")

        # Build the request string, encoding the parameters if necessary
        if params:
            request = f"{command} {' '.join([str(p) for p in params])}"
        else:
            request = command

        # Send the request and wait for the response as a single transaction
        async with self._command_lock:
            # Send the request
            self._writer.write(f"{request}\n".encode())
            await self._writer.drain()

            # Wait for the response
            response = await asyncio.wait_for(
                self._response_queue.get(), timeout=self._read_timeout
            )

        if isinstance(response, Exception):
            raise response

        return response

    async def events(self) -> AsyncIterator[str]:
        """
        An async iterator that yields events from the Host Command service.

        Yields:
            "S:" (Status) or "EL:" (Event Log) strings from the Host Command service.
        """

        queue = asyncio.Queue[Union[str, Exception]](1024)
        try:
            self._event_queues.add(queue)

            while True:
                event = await queue.get()
                if isinstance(event, Exception):
                    raise event

                yield event
        finally:
            self._event_queues.remove(queue)

    async def _message_handler(self) -> None:
        assert self._reader is not None

        while True:
            try:
                line = await self._reader.readuntil(self._delimiter)
                message = line.decode().rstrip()
                if message.startswith("R:ERROR"):
                    self._publish_response(command_error_from_string(message))
                    self._response_buffer = []
                elif message.startswith("R:"):
                    self._response_buffer.append(message)
                    self._publish_response(CommandResponse(self._response_buffer))
                    self._response_buffer = []
                elif message.startswith("S:") or message.startswith("EL:"):
                    self._publish_event(message)
                else:
                    self._response_buffer.append(message)
            except Exception as e:
                self._publish_response(e)
                self._publish_event(e)

                break

    def _publish_event(self, event: Union[str, Exception]) -> None:
        for queue in self._event_queues:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                self._logger.warning(f"Event queue full trying to put {event}")

    def _publish_response(self, response: Union[CommandResponse, Exception]) -> None:
        if self._command_lock.locked():
            self._response_queue.put_nowait(response)


class HostCommandClient:
    """
    High-level client to communicate with the Vantage InFusion "Host Command" service.

    This class handles connecting to the Host Command service, sending commands, and
    receiving events. It also provides helper methods for subscribing to various types
    of events, such as "STATUS" and "ELLOG".

    Internally, it uses one connection for sending commands, and a separate connection
    for receiving events. Both connections are created lazily when needed, and closed
    when the client is closed. The event handler connection will automatically reconnect
    if the connection is lost.
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        ssl: Union[SSLContext, bool] = True,
        port: Optional[int] = None,
        conn_timeout: Optional[float] = 5,
        read_timeout: Optional[float] = 10,
    ) -> None:
        """
        Initialize the HostCommandClient instance.

        Args:
            host: The hostname or IP address of the Host Command service.
            username: The username to use to authenticate, if required.
            password: The password to use to authenticate, if required.
            ssl: Whether to use SSL when connecting. If True, a default SSL context will
                be created. If False, SSL will not be used. If a SSLContext is provided,
                it will be used.
            port: The port to use when connecting. Defaults to 3010 if SSL is enabled,
                otherwise 3001.
            conn_timeout: The timeout to use when connecting, in seconds.
            read_timeout: The timeout to use when reading, in seconds.
        """

        self._host = host
        self._username = username
        self._password = password
        self._ssl = ssl
        self._port = port
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout

        self._command_connection: Optional[HostCommandConnection] = None
        self._event_handler_connection: Optional[HostCommandConnection] = None
        self._event_handler_connected: asyncio.Event = asyncio.Event()
        self._event_handler_task: Optional[asyncio.Task[None]] = None
        self._subscriptions: List[EventSubscription] = []
        self._subscribed_statuses: Dict[str, int] = defaultdict(int)
        self._subscribed_objects: Dict[int, int] = defaultdict(int)
        self._subscribed_event_logs: Dict[str, int] = defaultdict(int)
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> "HostCommandClient":
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
        Close the connections to the Host Command service and stop the event handler.
        """

        # Stop the event handler
        if self._event_handler_task is not None:
            self._event_handler_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._event_handler_task
            self._event_handler_task = None

        # Close the connections
        if self._event_handler_connection is not None:
            self._event_handler_connection.close()
            self._event_handler_connection = None

        if self._command_connection is not None:
            self._command_connection.close()
            self._command_connection = None

    async def command(
        self, command: str, *params: Union[int, float, str]
    ) -> CommandResponse:
        """
        Send a command with parameters to the Host Command service and wait for a
        response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command, int, float, or str.

        Returns:
            A CommandResponse instance.
        """

        if self._command_connection is None or self._command_connection.closed:
            self._command_connection = await self._create_connection()

        return await self._command_connection.command(command, *params)

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

        # Filter received status events by type
        def filtered_callback(event: Event) -> None:
            assert event["tag"] == EventType.STATUS
            if event["status_type"] in status_types:
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
                # Note: there's no nice way to ask the Host Command service to stop
                # sending status events of a particular type.
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
            assert event["tag"] == EventType.STATUS
            if event["id"] in object_ids:  # type: ignore[operator]
                callback(event)

        # Add the subscription to the list
        remove_subscription = self.subscribe(filtered_callback, EventType.STATUS)

        # Ask the controller to start sending status events for these objects
        conn = await self._get_event_handler_connection()
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

        # Ask the controller to start sending event logs for these types
        conn = await self._get_event_handler_connection()
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

    def _emit(self, event: Event) -> None:
        # Emit an event to subscribers

        for callback, event_types in self._subscriptions:
            if event_types is None or event["tag"] in event_types:
                if iscoroutinefunction(callback):
                    asyncio.create_task(callback(event))
                else:
                    callback(event)

    async def _get_event_handler_connection(self) -> HostCommandConnection:
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

    async def _create_connection(self, retry: bool = False) -> HostCommandConnection:
        # Get a new connection to the Host Command service, authenticating if necessary

        connect_attempts = 0
        while True:
            connect_attempts += 1

            try:
                conn = HostCommandConnection(
                    self._host,
                    self._port,
                    ssl=self._ssl,
                    conn_timeout=self._conn_timeout,
                    read_timeout=self._read_timeout,
                )
                await conn.open()

                # Log in if we have credentials
                if self._username is not None and self._password is not None:
                    await conn.command("LOGIN", self._username, self._password)

                return conn
            except (OSError, ConnectionError, SSLError, asyncio.TimeoutError):
                if not retry:
                    raise

            # Attempt to reconnect, with backoff
            reconnect_wait = min(2 * connect_attempts, 600)

            self._logger.debug(
                f"Connection to {self._host} failed"
                f" - retrying in {reconnect_wait} seconds"
            )

            if connect_attempts % 10 == 0:
                self._logger.warning(
                    f"{connect_attempts} attempts to (re)connect to {self._host} failed"
                    f" - this may indicate a problem with the connection"
                )

            await asyncio.sleep(reconnect_wait)

    async def _resubscribe(self, conn: HostCommandConnection) -> None:
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

        while True:
            try:
                # Get a connection, retrying if necessary
                conn = await self._create_connection(retry=True)
                self._event_handler_connection = conn

                # Signal that we're connected
                if self._event_handler_connected.is_set():
                    await self._resubscribe(conn)
                    self._emit({"tag": EventType.RECONNECTED})
                else:
                    self._event_handler_connected.set()
                    self._emit({"tag": EventType.CONNECTED})

                self._logger.info("Event handler connected and listening for events")

                # Start processing events
                async for event in conn.events():
                    self._logger.debug(f"Received event: {event}")

                    if event.startswith("S:"):
                        # Parse a status message
                        status_type, id_str, *args = tokenize_response(event)
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
                    elif event.startswith("EL:"):
                        # Parse an event log message
                        message = event[4:]

                        # Notify subscribers
                        self._emit(
                            {
                                "tag": EventType.EVENT_LOG,
                                "log": message,
                            },
                        )
                    else:
                        self._logger.warning(f"Received unexpected event: {event}")

            except (
                OSError,
                ConnectionError,
                SSLError,
                asyncio.TimeoutError,
                asyncio.IncompleteReadError,
            ):
                # If we get here, the connection was lost
                self._logger.debug("Event handler lost connection")
                self._emit({"tag": EventType.DISCONNECTED})

            except Exception as err:
                # Unexpected error, log for debugging
                self._logger.exception(err)
                raise err
