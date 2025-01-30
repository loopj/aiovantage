"""Subscribe to events from the Vantage Host Command service."""

import asyncio
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable, Iterable, Sequence
from contextlib import suppress
from enum import Enum
from inspect import iscoroutinefunction
from ssl import SSLContext
from types import TracebackType
from typing import Literal, TypedDict

from typing_extensions import Self

from aiovantage.errors import ClientConnectionError, ClientError

from .connection import CommandConnection
from .types import tokenize_response

# The interval between keepalive messages, in seconds.
KEEPALIVE_INTERVAL = 60


class EventType(Enum):
    """Enumeration of event types."""

    CONNECTED = "connect"
    DISCONNECTED = "disconnect"
    RECONNECTED = "reconnect"
    STATUS = "status"
    LOG = "log"
    ENHANCED_LOG = "enhanced_log"


class ConnectEvent(TypedDict):
    """Event emitted when the connection is established."""

    type: Literal[EventType.CONNECTED]


class DisconnectEvent(TypedDict):
    """Event emitted when the connection is lost."""

    type: Literal[EventType.DISCONNECTED]


class ReconnectEvent(TypedDict):
    """Event emitted when the connection is re-established."""

    type: Literal[EventType.RECONNECTED]


class StatusEvent(TypedDict):
    """Event emitted when a "S:" status is received."""

    type: Literal[EventType.STATUS]
    id: int
    category: str
    args: Sequence[str]


class EnhancedLogEvent(TypedDict):
    """Event emitted when an "EL:" enhanced log is received."""

    type: Literal[EventType.ENHANCED_LOG]
    log: str


# Type alias for any event type
Event = ConnectEvent | DisconnectEvent | ReconnectEvent | StatusEvent | EnhancedLogEvent

# Type aliases for callbacks for event subscriptions
EventCallback = Callable[[Event], Awaitable[None] | None]
EventFilter = Callable[[Event], bool]
EventSubscription = tuple[EventCallback, EventFilter | None]


class EventStream:
    """Client to subscribe to events from the Vantage Host Command service."""

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        *,
        ssl: SSLContext | bool = True,
        port: int | None = None,
        conn_timeout: float = 30,
    ) -> None:
        """Initialize the client."""
        self._connection = CommandConnection(host, port, ssl, conn_timeout)
        self._username = username
        self._password = password
        self._tasks: list[asyncio.Task[None]] = []
        self._subscriptions: list[EventSubscription] = []
        self._status_subscribers: dict[str, int] = defaultdict(int)
        self._enhanced_log_subscribers: dict[str, int] = defaultdict(int)
        self._start_lock = asyncio.Lock()
        self._started = False
        self._connection_lock = asyncio.Lock()
        self._command_queue: asyncio.Queue[str] = asyncio.Queue()
        self._logger = logging.getLogger(__name__)

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

    async def start(self) -> None:
        """Initialize the event stream."""
        async with self._start_lock:
            if self._started:
                return

            await self.get_connection()
            self._tasks.append(asyncio.create_task(self._message_handler()))
            self._tasks.append(asyncio.create_task(self._command_handler()))
            self._tasks.append(asyncio.create_task(self._keepalive()))

            self._logger.debug("Started the event stream")
            self._started = True

    def stop(self) -> None:
        """Stop the event stream."""
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
        self._connection.close()

        self._logger.debug("Stopped the event stream")
        self._started = False

    async def get_connection(self) -> CommandConnection:
        """Get a connection to the Host Command service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username and self._password:
                    await self._connection.authenticate(self._username, self._password)

                # Populate the capabilities of the connection (e.g. enhanced log support)
                await self._connection.populate_capabilities()

                self._logger.info(
                    "Connected to event stream at %s:%d",
                    self._connection.host,
                    self._connection.port,
                )

            return self._connection

    def subscribe(
        self,
        callback: EventCallback,
        event_filter: EventType | Iterable[EventType] | EventFilter | None = None,
    ) -> Callable[[], None]:
        """Subscribe to events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            event_filter: A filter to apply to events before invoking the callback.

        Returns:
            A function that can be used to unsubscribe from events.
        """
        # Support filtering by event type, a list of event types, or a predicate
        subscription: EventSubscription
        if isinstance(event_filter, EventType):
            subscription = (callback, lambda event: event["type"] == event_filter)
        elif isinstance(event_filter, Iterable):
            subscription = (callback, lambda event: event["type"] in event_filter)
        else:
            subscription = (callback, event_filter)

        self._subscriptions.append(subscription)

        # Return an unsubscribe callback to remove the subscription
        def unsubscribe() -> None:
            self._subscriptions.remove(subscription)

        return unsubscribe

    def subscribe_status(
        self, callback: EventCallback, *categories: str
    ) -> Callable[[], None]:
        """Subscribe to "Status" events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            *categories: The status categories to subscribe to events for.

        Returns:
            A coroutine that can be used to unsubscribe from status events.
        """
        # Enable this status type if it's not already enabled
        for category in categories:
            self._status_subscribers[category] += 1
            if self._status_subscribers[category] == 1:
                self._enable_status(category)

        # Subscribe, and return an unsubscribe callback
        remove_subscription = self.subscribe(
            callback,
            lambda event: (
                event["type"] == EventType.STATUS and event["category"] in categories
            ),
        )

        def unsubscribe() -> None:
            for category in categories:
                self._status_subscribers[category] -= 1
                if self._status_subscribers[category] == 0:
                    self._disable_status(category)
            remove_subscription()

        return unsubscribe

    def subscribe_enhanced_log(
        self, callback: EventCallback, *log_types: str
    ) -> Callable[[], None]:
        """Subscribe to "Enhanced Log" events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            log_types: The event log type or types to subscribe to.

        Returns:
            A coroutine that can be used to unsubscribe from log events.
        """
        # Enable this log type if it's not already enabled
        for log_type in log_types:
            self._enhanced_log_subscribers[log_type] += 1
            if self._enhanced_log_subscribers[log_type] == 1:
                self._enable_enhanced_log(log_type)

        # Subscribe, and return an unsubscribe callback
        remove_subscription = self.subscribe(callback, EventType.ENHANCED_LOG)

        def unsubscribe() -> None:
            for log_type in log_types:
                self._enhanced_log_subscribers[log_type] -= 1
                if self._enhanced_log_subscribers[log_type] == 0:
                    self._disable_enhanced_log(log_type)
            remove_subscription()

        return unsubscribe

    def emit(self, event: Event) -> None:
        """Emit an event to subscribers.

        Args:
            event: The event to emit.
        """
        for callback, event_filter in self._subscriptions:
            if event_filter is None or event_filter(event):
                if iscoroutinefunction(callback):
                    asyncio.create_task(callback(event))
                else:
                    callback(event)

    async def _message_handler(self) -> None:
        # Handle incoming messages from the Host Command service.
        connect_attempts = 0
        while True:
            connect_attempts += 1
            try:
                # Get the connection to the Host Command service
                conn = await self.get_connection()

                # Notify that we're connected
                if connect_attempts == 1:
                    self.emit({"type": EventType.CONNECTED})
                else:
                    self.emit({"type": EventType.RECONNECTED})
                    self._resubscribe()
                connect_attempts = 1

                # Wait for new messages
                while True:
                    message = await conn.readuntil(b"\r\n")
                    message = message.rstrip()
                    self._logger.debug("Received message: %s", message)
                    self._parse_message(message)

            except ClientConnectionError:
                pass  # Pass through to retry logic below

            # If we get here, the connection was lost
            self.emit({"type": EventType.DISCONNECTED})

            # Clear the command queue
            with suppress(asyncio.QueueEmpty):
                while not self._command_queue.empty():
                    self._command_queue.get_nowait()
                    self._command_queue.task_done()

            # Attempt to reconnect, with backoff
            reconnect_wait = min(2 * connect_attempts, 600)
            self._logger.debug(
                "Disconnected from EventStream - retrying in %d seconds",
                reconnect_wait,
            )

            # Log a warning every 10 attempts
            if connect_attempts % 10 == 0:
                self._logger.warning(
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
                self._logger.warning("Error while sending command: %s", str(err))

    async def _keepalive(self) -> None:
        # Send a periodic "ECHO" keepalive command.
        while True:
            await asyncio.sleep(KEEPALIVE_INTERVAL)

            try:
                await self._send("ECHO")
            except ClientError as err:
                self._logger.debug("Error while sending keepalive: %s", str(err))

    async def _send(self, message: str) -> None:
        # Send a plaintext message to the Host Command service."""
        self._logger.debug("Sending message: %s", message)
        await self._connection.write(f"{message}\n")

    def _parse_message(self, message: str) -> None:
        # Parse a message from the Host Command service.
        if message.startswith("S:"):
            # Parse a "status" message, of the form "S:<type> <id> <args>"
            # These messages are emitted when the state of an object changes after
            # subscribing to updates via "STATUS <type>" or "ADDSTATUS <vid>".
            category, id_str, *args = tokenize_response(message)
            self.emit(
                {
                    "type": EventType.STATUS,
                    "category": category[2:],
                    "id": int(id_str),
                    "args": args,
                }
            )
        elif message.startswith("EL:"):
            # Parse an "enhanced log" message, of the form "EL: <log>"
            # These messages are emitted when an enhanced log is received after
            # subscribing to updates via "ELLOG <type>".
            self.emit({"type": EventType.ENHANCED_LOG, "log": message[4:]})
        elif message.startswith("R:ERROR"):
            self._logger.error("Error message from EventStream: %s", message)

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
        for category, count in self._status_subscribers.items():
            if count > 0:
                self._queue_command(f"STATUS {category}")

    def _enable_enhanced_log(self, log_type: str) -> None:
        # Enable enhanced logging on the controller for a particular log type.
        controller_id: int = 1
        self._queue_command(f"ELAGG {controller_id} ON")
        self._queue_command(f"ELENABLE {controller_id} {log_type} ON")
        self._queue_command(f"ELLOG {log_type} ON")

    def _disable_enhanced_log(self, log_type: str) -> None:
        # Disable enhanced logging on the controller for a particular log type.
        controller_id: int = 1
        self._queue_command(f"ELENABLE {controller_id} {log_type} OFF")
        self._queue_command(f"ELLOG {log_type} OFF")

    def _resubscribe(self) -> None:
        # Re-subscribe to events after a reconnection.
        for category, count in self._status_subscribers.items():
            if count > 0:
                self._enable_status(category)

        for log_type, count in self._enhanced_log_subscribers.items():
            if count > 0:
                self._enable_enhanced_log(log_type)
