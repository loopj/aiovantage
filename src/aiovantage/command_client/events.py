"""Subscribe to events from the Vantage Host Command service."""

import asyncio
import logging
from collections import defaultdict
from contextlib import suppress
from enum import Enum
from inspect import iscoroutinefunction
from ssl import SSLContext
from types import TracebackType
from typing import (
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypedDict,
    Union,
)

from typing_extensions import Self

from aiovantage.errors import ClientConnectionError, ClientError

from .commands import CommandConnection
from .utils import tokenize_response

KEEPALIVE_INTERVAL = 60


# Typing for events
class EventType(Enum):
    """Enumeration of event types."""

    CONNECTED = "connect"
    DISCONNECTED = "disconnect"
    RECONNECTED = "reconnect"
    STATUS = "status"
    ENHANCED_LOG = "enhanced_log"


# Typed dictionaries for events
ConnectEvent = TypedDict("ConnectEvent", {"type": Literal[EventType.CONNECTED]})
DisconnectEvent = TypedDict(
    "DisconnectEvent", {"type": Literal[EventType.DISCONNECTED]}
)
ReconnectEvent = TypedDict("ReconnectEvent", {"type": Literal[EventType.RECONNECTED]})
StatusEvent = TypedDict(
    "StatusEvent",
    {
        "type": Literal[EventType.STATUS],
        "id": int,
        "status_type": str,
        "args": Sequence[str],
    },
)
EnhancedLogEvent = TypedDict(
    "EnhancedLogEvent", {"type": Literal[EventType.ENHANCED_LOG], "log": str}
)
Event = Union[
    ConnectEvent, DisconnectEvent, ReconnectEvent, StatusEvent, EnhancedLogEvent
]

# Type aliases for callbacks for event subscriptions
EventCallback = Callable[[Event], Union[None, Coroutine]]
EventFilter = Callable[[Event], bool]
EventSubscription = Tuple[EventCallback, Optional[EventFilter]]


class EventStream:
    """Client to subscribe to events from the Vantage Host Command service."""

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        ssl: Union[SSLContext, bool] = True,
        port: Optional[int] = None,
        conn_timeout: float = 30,
    ) -> None:
        """Initialize the client."""
        self._connection = CommandConnection(host, port, ssl, conn_timeout)
        self._username = username
        self._password = password
        self._tasks: List[asyncio.Task[None]] = []
        self._subscriptions: List[EventSubscription] = []
        self._status_subscribers: Dict[str, int] = defaultdict(int)
        self._enhanced_log_subscribers: Dict[str, int] = defaultdict(int)
        self._connection_lock = asyncio.Lock()
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> Self:
        """Return context manager."""
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        await self.stop()
        if exc_val:
            raise exc_val

    async def start(self) -> None:
        """Initialize the event stream."""
        await self.get_connection()
        self._tasks.append(asyncio.create_task(self._message_handler()))
        self._tasks.append(asyncio.create_task(self._keepalive()))

    async def stop(self) -> None:
        """Stop the event stream."""
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
        self._connection.close()

    async def get_connection(self) -> CommandConnection:
        """Get a connection to the Host Command service."""
        async with self._connection_lock:
            if self._connection.closed:
                # Open a new connection
                await self._connection.open()

                # Authenticate the new connection if we have credentials
                if self._username is not None and self._password is not None:
                    await self._send(f"LOGIN {self._username} {self._password}")

            return self._connection

    def subscribe(
        self,
        callback: EventCallback,
        event_filter: Union[EventType, Iterable[EventType], EventFilter, None] = None,
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
            subscription = (callback, lambda event: event["type"] in event_filter)  # type: ignore[operator]
        else:
            subscription = (callback, event_filter)

        self._subscriptions.append(subscription)

        # Return an unsubscribe callback to remove the subscription
        def unsubscribe() -> None:
            self._subscriptions.remove(subscription)

        return unsubscribe

    async def subscribe_status(
        self, callback: EventCallback, status_type: str
    ) -> Callable[[], Awaitable[None]]:
        """Subscribe to "Status" events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            status_type: The type of status to subscribe to.

        Returns:
            A coroutine that can be used to unsubscribe from status events.
        """

        # Enable this status type if it's not already enabled
        self._status_subscribers[status_type] += 1
        if self._status_subscribers[status_type] == 1:
            await self._enable_status(status_type)

        # Subscribe, and return an unsubscribe callback
        remove_subscription = self.subscribe(
            callback,
            lambda event: (
                event["type"] == EventType.STATUS
                and event["status_type"] == status_type
            ),
        )

        async def unsubscribe() -> None:
            self._status_subscribers[status_type] -= 1
            if self._status_subscribers[status_type] == 0:
                await self._disable_status(status_type)
            remove_subscription()

        return unsubscribe

    async def subscribe_enhanced_log(
        self, callback: EventCallback, log_type: str
    ) -> Callable[[], Awaitable[None]]:
        """Subscribe to "Enhanced Log" events from the Host Command service.

        Args:
            callback: The callback to invoke when an event is received.
            log_type: The type of log to subscribe to.

        Returns:
            A coroutine that can be used to unsubscribe from log events.
        """

        # Enable this log type if it's not already enabled
        self._enhanced_log_subscribers[log_type] += 1
        if self._enhanced_log_subscribers[log_type] == 1:
            await self._enable_enhanced_log(log_type)

        # Subscribe, and return an unsubscribe callback
        remove_subscription = self.subscribe(callback, EventType.ENHANCED_LOG)

        async def unsubscribe() -> None:
            self._enhanced_log_subscribers[log_type] -= 1
            if self._enhanced_log_subscribers[log_type] == 0:
                await self._disable_enhanced_log(log_type)
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
                self._logger.debug("Connected to EventStream")
                if connect_attempts == 1:
                    self.emit({"type": EventType.CONNECTED})
                else:
                    self.emit({"type": EventType.RECONNECTED})
                    await self._resubscribe()
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

    async def _keepalive(self) -> None:
        # Send a periodic "ECHO" keepalive command.
        while True:
            await asyncio.sleep(KEEPALIVE_INTERVAL)

            try:
                await self._send("ECHO")
            except ClientError as err:
                self._logger.debug("Error while sending keepalive: %s", str(err))

    def _parse_message(self, message: str) -> None:
        # Parse a message from the Host Command service.
        if message.startswith("S:"):
            # Parse a "Status" message
            status_type, id_str, *args = tokenize_response(message)
            self.emit(
                {
                    "type": EventType.STATUS,
                    "status_type": status_type[2:],
                    "id": int(id_str),
                    "args": args,
                }
            )
        elif message.startswith("EL:"):
            # Parse an "Enhanced Log" message
            self.emit({"type": EventType.ENHANCED_LOG, "log": message[4:]})
        elif message.startswith("R:ERROR"):
            self._logger.error("Error message from EventStream: %s", message)

    async def _send(self, message: str) -> None:
        # Send a plaintext message to the Host Command service."""
        self._logger.debug("Sending message: %s", message)
        await self._connection.write(f"{message}\n")

    async def _enable_status(self, status_type: str) -> None:
        # Enable status updates on the controller for a particular status type.
        await self._send(f"STATUS {status_type}")

    async def _disable_status(self, status_type: str) -> None:
        # Note: there's no nice way to ask the Host Command service to stop
        # sending status events of a single type.
        pass

    async def _enable_enhanced_log(self, log_type: str) -> None:
        # Enable enhanced logging on the controller for a particular log type.
        await self._send("ELAGG 1 ON")
        await self._send(f"ELENABLE {log_type} ON")
        await self._send(f"ELLOG {log_type} ON")

    async def _disable_enhanced_log(self, log_type: str) -> None:
        # Disable enhanced logging on the controller for a particular log type.
        with suppress(ClientConnectionError):
            await self._send(f"ELLOG {log_type} OFF")

    async def _resubscribe(self) -> None:
        # Re-subscribe to events after a reconnection.
        for status_type, count in self._status_subscribers.items():
            if count > 0:
                await self._enable_status(status_type)

        for log_type, count in self._enhanced_log_subscribers.items():
            if count > 0:
                await self._enable_enhanced_log(log_type)
