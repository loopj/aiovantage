import asyncio
from collections import Counter, defaultdict
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from ssl import SSLContext
from types import TracebackType
from typing import TypeVar

from typing_extensions import Self

from aiovantage._logger import logger
from aiovantage.errors import ClientConnectionError, ClientError

from .connection import CommandConnection
from .converter import Converter

T = TypeVar("T")

# The interval between keepalive messages, in seconds.
KEEPALIVE_INTERVAL = 60


@dataclass
class Event:
    """Base class for events emitted by the EventStream."""


@dataclass
class ConnectEvent(Event):
    """Event emitted when the connection is established."""


@dataclass
class DisconnectEvent(Event):
    """Event emitted when the connection is lost."""


@dataclass
class ReconnectEvent(Event):
    """Event emitted when the connection is re-established."""


@dataclass
class StatusEvent(Event):
    """Event emitted when a "S:" status is received."""

    category: str
    """The status category, eg. "LOAD", "BLIND", etc."""

    vid: int
    """The unique Vantage ID of the object the status applies to."""

    args: list[str]
    """The arguments of the status message."""


@dataclass
class EnhancedLogEvent(Event):
    """Event emitted when an "EL:" enhanced log is received."""

    log: str
    """The enhanced log message."""


class EventStream:
    """Client to subscribe to events from the Vantage Host Command (HC) service.

    Args:
        host: The hostname or IP address of the Vantage controller.
        username: The username to use for authentication.
        password: The password to use for authentication.
        ssl: The SSL context to use. True will use a default context, False will disable SSL.
        ssl_context_factory: A factory function to use when creating default SSL contexts.
        port: The port to connect to.
        conn_timeout: The connection timeout in seconds.
    """

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        *,
        ssl: SSLContext | bool = True,
        ssl_context_factory: Callable[[], SSLContext] | None = None,
        port: int | None = None,
        conn_timeout: float = 30,
    ) -> None:
        """Initialize the client."""
        self._connection = CommandConnection(
            host,
            port=port,
            ssl=ssl,
            ssl_context_factory=ssl_context_factory,
            conn_timeout=conn_timeout,
        )

        self._username = username
        self._password = password
        self._tasks: list[asyncio.Task[None]] = []
        self._start_lock = asyncio.Lock()
        self._started = False
        self._connection_lock = asyncio.Lock()
        self._command_queue: asyncio.Queue[str] = asyncio.Queue()

        self._subscriptions: dict[type[Event], set[Callable[[Event], None]]] = (
            defaultdict(set)
        )

        self._status_counts: StatusCounter[str] = StatusCounter(
            on_first_add=self._enable_status,
            on_last_remove=self._disable_status,
        )

        self._enhanced_log_counts: StatusCounter[str] = StatusCounter(
            on_first_add=self._enable_enhanced_log,
            on_last_remove=self._disable_enhanced_log,
        )

    async def __aenter__(self) -> Self:
        """Return context manager."""
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self.stop()
        if exc_val:
            raise exc_val

    async def start(self) -> CommandConnection:
        """Initialize the event stream."""
        async with self._start_lock:
            # Get the connection to the Host Command service
            conn = await self._get_connection()

            # Start the event stream tasks
            if not self._started:
                self._tasks.append(asyncio.create_task(self._message_handler()))
                self._tasks.append(asyncio.create_task(self._command_handler()))
                self._tasks.append(asyncio.create_task(self._keepalive()))

                logger.debug("Started the event stream")
                self._started = True

            return conn

    def stop(self) -> None:
        """Stop the event stream."""
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
        self._connection.close()

        logger.debug("Stopped the event stream")
        self._started = False

    async def _get_connection(self) -> CommandConnection:
        """Get a connection to the Host Command service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username and self._password:
                    await self._connection.authenticate(self._username, self._password)

                logger.info(
                    "Connected to event stream at %s:%d",
                    self._connection.host,
                    self._connection.port,
                )

            return self._connection

    def subscribe(
        self, callback: Callable[[Event], None], *event_types: type[Event]
    ) -> Callable[[], None]:
        """Subscribe to events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            event_types: The event types to subscribe to.

        Returns:
            A function that can be used to unsubscribe from events.
        """
        # Support filtering by event types
        for event_type in event_types:
            self._subscriptions[event_type].add(callback)

        # Return an unsubscribe callback to remove the subscription
        def unsubscribe() -> None:
            for event_type in event_types:
                self._subscriptions[event_type].remove(callback)

        return unsubscribe

    def subscribe_status(
        self, callback: Callable[[Event], None], *categories: str
    ) -> Callable[[], None]:
        """Subscribe to "Status" events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            *categories: The status categories to subscribe to events for.

        Returns:
            A function that can be used to unsubscribe from status events.
        """
        if not categories:
            categories = ("ALL",)

        # Enable this status type if it's not already enabled
        self._status_counts.update(categories)

        # Filter events by category
        def _callback(event: Event) -> None:
            if not isinstance(event, StatusEvent):
                return

            if "ALL" in categories or event.category in categories:
                callback(event)

        # Subscribe, and return an unsubscribe callback
        remove_subscription = self.subscribe(_callback, StatusEvent)

        def unsubscribe() -> None:
            self._status_counts.subtract(categories)
            remove_subscription()

        return unsubscribe

    def subscribe_enhanced_log(
        self, callback: Callable[[Event], None], *log_types: str
    ) -> Callable[[], None]:
        """Subscribe to "Enhanced Log" events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            log_types: The event log type or types to subscribe to.

        Returns:
            A function that can be used to unsubscribe from log events.
        """
        # Enable this log type if it's not already enabled
        self._enhanced_log_counts.update(log_types)

        # Subscribe, and return an unsubscribe callback
        remove_subscription = self.subscribe(callback, EnhancedLogEvent)

        def unsubscribe() -> None:
            self._enhanced_log_counts.subtract(log_types)
            remove_subscription()

        return unsubscribe

    def _emit(self, event: Event) -> None:
        # Emit an event to subscribers.
        for callback in self._subscriptions[type(event)]:
            callback(event)

    async def _message_handler(self) -> None:
        # Handle incoming messages from the Host Command service.
        connect_attempts = 0
        while True:
            connect_attempts += 1
            try:
                # Get the connection to the Host Command service
                conn = await self._get_connection()

                # Notify that we're connected
                if connect_attempts == 1:
                    self._emit(ConnectEvent())
                else:
                    self._emit(ReconnectEvent())
                    self._resubscribe()
                connect_attempts = 1

                # Wait for new messages
                while True:
                    message = await conn.readuntil(b"\r\n")
                    message = message.rstrip()
                    logger.debug("Received message: %s", message)
                    self._parse_message(message)

            except ClientConnectionError:
                pass  # Pass through to retry logic below

            # If we get here, the connection was lost
            if connect_attempts == 1:
                self._emit(DisconnectEvent())

            # Clear the command queue
            with suppress(asyncio.QueueEmpty):
                while not self._command_queue.empty():
                    self._command_queue.get_nowait()
                    self._command_queue.task_done()

            # Attempt to reconnect, with backoff
            reconnect_wait = min(2 * connect_attempts, 600)
            logger.debug(
                "Disconnected from EventStream - retrying in %d seconds",
                reconnect_wait,
            )

            # Log a warning every 10 attempts
            if connect_attempts % 10 == 0:
                logger.warning(
                    "%d attempts to (re)connect to controller failed"
                    " - This might be an indication of connection issues.",
                    connect_attempts,
                )

            await asyncio.sleep(reconnect_wait)

    async def _command_handler(self) -> None:
        # Handle outgoing commands to the Host Command service.
        while True:
            try:
                command = await self._command_queue.get()
                await self._send(command)
                self._command_queue.task_done()
            except ClientError as err:
                logger.warning("Error while sending command: %s", str(err))

    async def _keepalive(self) -> None:
        # Send a periodic "ECHO" keepalive command.
        while True:
            await asyncio.sleep(KEEPALIVE_INTERVAL)

            try:
                await self._send("ECHO")
            except ClientError as err:
                logger.debug("Error while sending keepalive: %s", str(err))

    async def _send(self, message: str) -> None:
        # Send a plaintext message to the Host Command service."""
        logger.debug("Sending message: %s", message)
        await self._connection.write(f"{message}\n")

    def _parse_message(self, message: str) -> None:
        # Parse a message from the Host Command service.
        if message.startswith("S:"):
            # Parse a "status" message, of the form "S:<type> <vid> <args>"
            # These messages are emitted when the state of an object changes after
            # subscribing to updates via "STATUS <type>" or "ADDSTATUS <vid>".
            category, vid_str, *args = Converter.tokenize(message)
            self._emit(StatusEvent(category[2:], int(vid_str), args))

        elif message.startswith("EL: "):
            # Parse an "enhanced log" message, of the form "EL: <log>"
            # These messages are emitted when an enhanced log is received after
            # subscribing to updates via "ELLOG <type>".
            self._emit(EnhancedLogEvent(message[4:]))

        elif message.startswith("R:ERROR"):
            logger.error("Error message from EventStream: %s", message)

    def _queue_command(self, command: str) -> None:
        # Queue a command to be sent to the Host Command service.
        self._command_queue.put_nowait(command)

    def _enable_status(self, category: str) -> None:
        # Enable status updates on the controller for a particular status type.
        self._queue_command(f"STATUS {category}")

    def _disable_status(self, _category: str) -> None:
        # Disable status updates on the controller for a particular status type.
        # Note: This assumes the count has already been decremented.
        self._queue_command("STATUS NONE")
        for category, count in self._status_counts.items():
            if count > 0:
                self._enable_status(category)

    def _enable_enhanced_log(self, log_type: str) -> None:
        # Enable enhanced logging on the controller for a particular log type.
        self._queue_command("ELAGG 1 ON")
        self._queue_command(f"ELENABLE 1 {log_type} ON")
        self._queue_command(f"ELLOG {log_type} ON")

    def _disable_enhanced_log(self, log_type: str) -> None:
        # Disable enhanced logging on the controller for a particular log type.
        self._queue_command(f"ELENABLE 1 {log_type} OFF")
        self._queue_command(f"ELLOG {log_type} OFF")

    def _resubscribe(self) -> None:
        # Re-subscribe to events after a reconnection.
        for category, count in self._status_counts.items():
            if count > 0:
                self._enable_status(category)

        for log_type, count in self._enhanced_log_counts.items():
            if count > 0:
                self._enable_enhanced_log(log_type)


class StatusCounter(Counter[T]):
    """Reference-counter for status types."""

    def __init__(
        self, on_first_add: Callable[[T], None], on_last_remove: Callable[[T], None]
    ) -> None:
        super().__init__()
        self._on_first_add = on_first_add
        self._on_last_remove = on_last_remove

    def __setitem__(self, key: T, value: int) -> None:
        previous = self.get(key, 0)
        super().__setitem__(key, value)

        if previous == 0 and value > 0:
            self._on_first_add(key)
        elif previous > 0 and value <= 0:
            self._on_last_remove(key)
            del self[key]
