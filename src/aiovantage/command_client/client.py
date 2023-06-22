"""Client to communicate with the Host Command service."""

import asyncio
import logging
from collections import defaultdict
from contextlib import suppress
from decimal import Decimal
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
    Optional,
    Tuple,
    Type,
    Union,
)

from typing_extensions import Self

from .connection import CommandConnection
from .errors import ClientConnectionError, ClientError, ClientTimeoutError
from .events import Event, EventType
from .response import CommandResponse
from .utils import tokenize_response

# Constants
KEEPALIVE_INTERVAL = 60

# Type aliases for callbacks for event subscriptions
EventCallback = Callable[[Event], Union[None, Coroutine]]
EventFilter = Callable[[Event], bool]
EventSubscription = Tuple[EventCallback, Optional[EventFilter]]


class CommandClient:
    """Client to communicate with the Host Command service.

    This class handles connecting to the Host Command service, sending commands, and
    receiving events. It also provides helper methods for subscribing to various types
    of events, such as "STATUS" and "ELLOG".

    Connections are created lazily when needed, and closed when the client is closed,
    and will automatically reconnect if the connection is lost.
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
        """Initialize the CommandClient instance.

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

        self._connection: Optional[CommandConnection] = None
        self._event_handler_task: Optional[asyncio.Task[None]] = None
        self._event_handler_ready: asyncio.Event = asyncio.Event()
        self._keepalive_task: Optional[asyncio.Task[None]] = None
        self._subscriptions: List[EventSubscription] = []
        self._subscribed_statuses: Dict[str, int] = defaultdict(int)
        self._subscribed_objects: Dict[int, int] = defaultdict(int)
        self._subscribed_event_logs: Dict[str, int] = defaultdict(int)
        self._logger = logging.getLogger(__name__)
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> Self:
        """Return context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        await self.close()
        if exc_val:
            raise exc_val

    async def connection(self, retry: bool = False) -> CommandConnection:
        """Get a connection to the Host Command service, creating one if necessary.

        Args:
            retry: Whether to retry if the connection attempt fails.
        """

        try:
            # Note: Getting a connection can potentially block for a long time even if
            # retry is False, if someone else is already trying to get a connection.
            await asyncio.wait_for(
                self._lock.acquire(), timeout=(None if retry else self._conn_timeout)
            )
        except asyncio.TimeoutError as exc:
            raise ClientTimeoutError("Timeout waiting for connection") from exc

        try:
            if self._connection is None or self._connection.closed:
                self._connection = await self._create_connection(retry=retry)

            return self._connection
        finally:
            self._lock.release()

    async def close(self) -> None:
        """Close the connections to the Host Command service and cancel any running tasks."""

        # Cancel the keepalive task
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
            self._keepalive_task = None

        # Cancel the event handler task
        if self._event_handler_task is not None:
            self._event_handler_task.cancel()
            self._event_handler_task = None

        # Close the connections
        if self._connection is not None:
            self._connection.close()

    async def command(
        self,
        command: str,
        *params: Union[str, int, float, Decimal, bool],
        force_quotes: bool = False,
    ) -> CommandResponse:
        """Send a command to the Host Command service and wait for a response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command.
            force_quotes: Whether to force string params to be wrapped in double quotes.

        Returns:
            A CommandResponse instance.
        """

        conn = await self.connection()
        return await conn.command(command, *params, force_quotes=force_quotes)

    def subscribe(
        self,
        callback: EventCallback,
        event_filter: Union[EventType, Iterable[EventType], EventFilter, None] = None,
    ) -> Callable[[], None]:
        """Subscribe to Host Command events, optionally filtering by event type.

        Args:
            callback: The callback to call when an event is received.
            event_filter: The event type(s) to filter by, or None to receive all events.

        Returns:
            A callback that can be called to unsubscribe.
        """

        # Support filtering by event type, a list of event types, or a predicate
        # TODO: Declaration "filter_fn" is obscured by a declaration of the same name
        filter_fn: Optional[EventFilter]
        if isinstance(event_filter, EventType):

            def filter_fn(event: Event) -> bool:
                return event["tag"] == event_filter

        elif isinstance(event_filter, Iterable):

            def filter_fn(event: Event) -> bool:
                return event["tag"] in event_filter

        else:
            # TODO: Expression of type "EventFilter | None" cannot be assigned to declared type "(event: Event) -> bool"
            filter_fn = event_filter

        # Add the subscription
        subscription: EventSubscription = (callback, filter_fn)
        self._subscriptions.append(subscription)

        # Return an unsubscribe callback to remove the subscription
        def unsubscribe() -> None:
            self._subscriptions.remove(subscription)

        return unsubscribe

    async def subscribe_status(
        self, callback: EventCallback, status_types: Union[str, Iterable[str]]
    ) -> Callable[[], Awaitable[None]]:
        """Subscribe to status events for the given status types, using "STATUS {type}".

        Args:
            callback: The callback to call when a status event is received.
            status_types: The status types to subscribe to status events for.

        Returns:
            A coroutine to unsubscribe from status events.
        """

        # Start the event handler if it's not already running
        await self._start_event_handler()

        # Support both a single status type and a list of status types
        if isinstance(status_types, str):
            status_types = (status_types,)

        # Filter received status events by type
        def event_filter(event: Event) -> bool:
            return (
                event["tag"] == EventType.STATUS
                and event["status_type"] in status_types
            )

        # Add the subscription to the list
        remove_subscription = self.subscribe(callback, event_filter)

        # Ask the Host Command service to start sending status events
        conn = await self.connection()
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
        """Subscribe to status events for the given object ids, using "ADDSTATUS {id}".

        Args:
            callback: The callback to call when a status event is received.
            object_ids: The ids to subscribe to status events for.

        Returns:
            A coroutine to unsubscribe from status events.
        """

        # Start the event handler if it's not already running
        await self._start_event_handler()

        # Support both a single object id and a list of object ids
        if isinstance(object_ids, int):
            object_ids = (object_ids,)

        # Filter received status events by id
        def event_filter(event: Event) -> bool:
            return event["tag"] == EventType.STATUS and event["id"] in object_ids

        # Add the subscription to the list
        remove_subscription = self.subscribe(callback, event_filter)

        # Ask the controller to start sending status events for these objects
        conn = await self.connection()
        for object_id in object_ids:
            self._subscribed_objects[object_id] += 1
            if self._subscribed_objects[object_id] == 1:
                await conn.command("ADDSTATUS", object_id)

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            with suppress(ClientConnectionError):
                for object_id in object_ids:
                    self._subscribed_objects[object_id] -= 1
                    if self._subscribed_objects[object_id] == 0:
                        await conn.command("DELSTATUS", object_id)

            remove_subscription()

        return unsubscribe

    async def subscribe_event_log(
        self, callback: EventCallback, log_types: Union[str, Iterable[str]]
    ) -> Callable[[], Awaitable[None]]:
        """Subscribe to event log events, using "ELLOG {type} ON".

        Args:
            callback: The callback to call when an event log event is received.
            log_types: The event log types to subscribe to.

        Returns:
            A coroutine to unsubscribe from event log events.
        """

        # Start the event handler if it's not already running
        await self._start_event_handler()

        # Support both a single log type and a list of log types
        if isinstance(log_types, str):
            log_types = (log_types,)

        # Add the subscription to the list
        remove_subscription = self.subscribe(callback, EventType.EVENT_LOG)

        # Get the connection
        conn = await self.connection()

        # Enable the event log
        await conn.command("ELAGG ON")

        # Ask the controller to start sending event logs for these types
        for log_type in log_types:
            self._subscribed_event_logs[log_type] += 1
            if self._subscribed_event_logs[log_type] == 1:
                await conn.command("ELENABLE", log_type, "ON")
                await conn.command("ELLOG", log_type, "ON")

        # Return an unsubscribe callback
        async def unsubscribe() -> None:
            with suppress(ClientConnectionError):
                for log_type in log_types:
                    self._subscribed_event_logs[log_type] -= 1
                    if self._subscribed_event_logs[log_type] == 0:
                        await conn.command("ELLOG", log_type, "OFF")

            remove_subscription()

        return unsubscribe

    def _emit(self, event: Event) -> None:
        # Emit an event to any subscribers that are interested in it

        for callback, event_filter in self._subscriptions:
            if event_filter is None or event_filter(event):
                if iscoroutinefunction(callback):
                    asyncio.create_task(callback(event))  # noqa: RUF006
                else:
                    callback(event)

    async def _start_event_handler(self) -> None:
        # Start the event handler if it's not already running

        if self._event_handler_task is None or self._event_handler_task.done():
            self._event_handler_task = asyncio.create_task(self._event_handler())
            await self._event_handler_ready.wait()

    async def _create_connection(self, retry: bool = False) -> CommandConnection:
        # Get a new connection to the Host Command service, authenticating if necessary

        connect_attempts = 0
        while True:
            connect_attempts += 1

            try:
                conn = CommandConnection(
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
            except ClientConnectionError:
                if not retry:
                    raise

            # Attempt to reconnect, with backoff
            reconnect_wait = min(2 * connect_attempts, 600)

            self._logger.debug(
                "Connection to controller failed - retrying in %d seconds",
                reconnect_wait,
            )

            if connect_attempts % 10 == 0:
                self._logger.warning(
                    "%d attempts to (re)connect to controller failed"
                    " - This might be an indication of connection issues.",
                    connect_attempts,
                )

            await asyncio.sleep(reconnect_wait)

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

        while True:
            try:
                # Get a connection, retrying if necessary
                conn = await self.connection(retry=True)

                # Signal that we're connected
                if self._event_handler_ready.is_set():
                    await self._resubscribe(conn)
                    self._emit({"tag": EventType.RECONNECTED})
                else:
                    self._event_handler_ready.set()
                    self._emit({"tag": EventType.CONNECTED})

                self._logger.info("Event handler connected and listening for events")

                # Start the keepalive task
                self._keepalive_task = asyncio.create_task(self._keepalive())

                # Start processing events
                async for event in conn.events():
                    self._logger.debug("Received event: %s", event)

                    if event.startswith("S:"):
                        # Parse a status message
                        status_type, id_str, *args = tokenize_response(event)
                        status_type = status_type[2:]

                        # Notify subscribers
                        self._emit(
                            {
                                "tag": EventType.STATUS,
                                "status_type": status_type,
                                "id": int(id_str),
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
                        self._logger.warning("Received unexpected event: %s", event)

            except ClientConnectionError:
                pass

            except Exception:
                # Unexpected error, log for debugging
                self._logger.exception("Unexpected error in event handler")
                raise

            # If we get here, the connection was lost
            self._logger.debug("Event handler lost connection")
            self._emit({"tag": EventType.DISCONNECTED})

            # Cancel the keepalive task
            if self._keepalive_task is not None:
                self._keepalive_task.cancel()
                self._keepalive_task = None

    async def _keepalive(self) -> None:
        # Send an "ECHO" command periodically to keep the connection alive,
        # and detect dropped connections.

        while True:
            await asyncio.sleep(KEEPALIVE_INTERVAL)

            try:
                await self.command("ECHO")
            except ClientError as err:
                self._logger.debug("Error while sending keepalive: %s", str(err))
