"""Base controller for Vantage objects."""

import asyncio
import logging
from abc import abstractmethod
from inspect import iscoroutinefunction
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from aiovantage.command_client import CommandClient, Event, EventType
from aiovantage.command_client.utils import tokenize_response
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects
from aiovantage.config_client.objects import SystemObject
from aiovantage.events import VantageEvent
from aiovantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage import Vantage

T = TypeVar("T", bound=SystemObject)


# Types for callbacks for event subscriptions
EventCallback = Callable[[VantageEvent, T, Dict[str, Any]], None]
EventSubscription = Tuple[EventCallback[T], Optional[Iterable[VantageEvent]]]


class BaseController(QuerySet[T]):
    """Base controller for Vantage objects."""

    # The Vantage object types that this controller handles
    vantage_types: Tuple[str, ...]

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize instance."""
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscriptions: List[EventSubscription[T]] = []
        self._id_subscriptions: Dict[int, List[EventSubscription[T]]] = {}
        self._initialized = False

        QuerySet.__init__(self, self._items, self.initialize)

        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initialization hook."""

    def __getitem__(self, vid: int) -> T:
        """Return the object with the given Vantage ID."""
        return self._items[vid]

    def __contains__(self, vid: int) -> bool:
        """Return True if the object with the given Vantage ID exists."""
        return vid in self._items

    @property
    def config_client(self) -> ConfigClient:
        """Return the config client instance."""
        return self._vantage.config_client

    @property
    def command_client(self) -> CommandClient:
        """Return the command client instance."""
        return self._vantage.command_client

    async def initialize(self) -> None:
        """Initialize a stateless controller by populating the objects it manages."""

        if self._initialized:
            return

        await self.fetch_objects()

        self._initialized = True

    async def fetch_objects(self) -> None:
        """Fetch all objects managed by this controller."""

        async for obj in get_objects(self.config_client, types=self.vantage_types):
            self._items[obj.id] = cast(T, obj)
            self.emit(VantageEvent.OBJECT_ADDED, cast(T, obj))

        self._logger.info("%s fetched objects", self.__class__.__name__)

    def subscribe(
        self,
        callback: EventCallback[T],
        id_filter: Union[int, Tuple[int], None] = None,
        event_filter: Union[VantageEvent, Tuple[VantageEvent], None] = None,
    ) -> Callable[[], None]:
        """Subscribe to status changes for objects managed by this controller.

        Args:
            callback: The callback to call when an object changes.
            id_filter: The Vantage IDs to subscribe to, all objects if None.
            event_filter: The event types to subscribe to, all events if None.

        Returns:
            A function to unsubscribe from the callback.
        """

        # Handle single ID filter
        if isinstance(id_filter, int):
            id_filter = (id_filter,)

        # Handle single event filter
        if isinstance(event_filter, VantageEvent):
            event_filter = (event_filter,)

        # Create the subscription
        subscription = (callback, event_filter)

        # Add the subscription to the list of subscriptions
        if id_filter is None:
            self._subscriptions.append(subscription)
        else:
            for vid in id_filter:
                if vid not in self._id_subscriptions:
                    self._id_subscriptions[vid] = []
                self._id_subscriptions[vid].append(subscription)

        # Return a function to unsubscribe
        def unsubscribe() -> None:
            if id_filter is None:
                self._subscriptions.remove(subscription)
            else:
                for vid in id_filter:
                    if vid not in self._id_subscriptions:
                        continue
                    self._id_subscriptions[vid].remove(subscription)

        return unsubscribe

    def emit(
        self,
        event_type: VantageEvent,
        obj: T,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Emit an event to subscribers of this controller.

        Args:
            event_type: The type of event to emit.
            obj: The object that the event relates to.
            data: Data to pass to the callback.
        """

        if data is None:
            data = {}

        # Grab a list of subscribers that care about this object
        subscribers = self._subscriptions + self._id_subscriptions.get(obj.id, [])
        for callback, event_filter in subscribers:
            if event_filter is not None and event_type not in event_filter:
                continue

            if iscoroutinefunction(callback):
                asyncio.create_task(callback(event_type, obj, data))  # noqa: RUF006
            else:
                callback(event_type, obj, data)


class StatefulController(BaseController[T]):
    """Base controller for Vantage objects that have state."""

    # Which Vantage status types this controller handles, if any
    status_types: Optional[Tuple[str, ...]] = None

    # Should we subscribe to status updates from the event log?
    event_log_status: bool = False

    # Which status methods this controller handles from the event log
    event_log_status_methods: Optional[Tuple[str, ...]] = None

    @abstractmethod
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of an object."""

    @abstractmethod
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for an object."""

    async def initialize(self) -> None:
        """Initialize a stateful controller.

        Populates the objects it manages, fetches their initial state, and subscribes
        to state updates.
        """

        if self._initialized:
            return

        await self.fetch_objects()
        await self.fetch_full_state()
        await self.subscribe_to_updates()

        self.command_client.subscribe(
            self._handle_command_client_event, EventType.RECONNECTED
        )

        self._initialized = True

    async def fetch_full_state(self) -> None:
        """Fetch the full state of all objects managed by this controller."""

        await asyncio.gather(
            *[self.fetch_object_state(obj.id) for obj in self._items.values()]
        )

        self._logger.info("%s fetched full state", self.__class__.__name__)

    async def subscribe_to_updates(self) -> None:
        """Subscribe to state updates for objects managed by this controller."""

        if not self._items:
            return

        # Subscribe to object state updates from the event log
        if self.event_log_status:
            await self.command_client.subscribe_event_log(
                self._handle_command_client_event, ("STATUS", "STATUSEX")
            )

        # Subscribe to "STATUS {type}" updates, if this controller cares about them
        if self.status_types:
            await self.command_client.subscribe_status(
                self._handle_command_client_event, self.status_types
            )

        self._logger.info("%s subscribed to updates", self.__class__.__name__)

    def update_state(self, vid: int, state: Dict[str, Any]) -> None:
        """Update the state of an object and notify subscribers if it changed.

        Args:
            vid: The Vantage ID of the object to update.
            state: A dictionary of attributes to update.
        """

        # Get the object, skip if it doesn't exist
        obj = self.get(vid)
        if obj is None:
            return

        # Check if any of the attributes changed and update them
        attrs_changed = []
        for key, value in state.items():
            try:
                if getattr(obj, key) != value:
                    setattr(obj, key, value)
                    attrs_changed.append(key)
            except AttributeError:
                self._logger.warning("Object '%d' has no attribute '%s'", obj.id, key)

        # Notify subscribers if any attributes changed
        if len(attrs_changed) > 0:
            self.emit(
                VantageEvent.OBJECT_UPDATED,
                obj,
                {"attrs_changed": attrs_changed},
            )

    async def _handle_command_client_event(self, event: Event) -> None:
        # Handle status update events from the command client

        if event["tag"] == EventType.STATUS:
            # Handle "STATUS {type}" events

            if event["id"] not in self._items:
                return

            self.handle_object_update(event["id"], event["status_type"], event["args"])

        elif event["tag"] == EventType.EVENT_LOG:
            # Handle event log events

            # Filter out events that this controller doesn't care about
            id_str, method, *args = tokenize_response(event["log"])
            if (
                self.event_log_status_methods
                and method not in self.event_log_status_methods
            ):
                return

            vid = int(id_str)
            if vid not in self._items:
                return

            # Pass the event to the controller
            self.handle_object_update(vid, method, args)

        elif event["tag"] == EventType.RECONNECTED:
            # Handle reconnect events

            # Fetch the full state
            await self.fetch_full_state()
