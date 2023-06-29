"""Base controller for Vantage objects."""

import asyncio
import logging
from dataclasses import fields
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
)

from aiovantage.command_client import CommandClient, Event, EventStream, EventType
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

    vantage_types: Tuple[str, ...]
    """The Vantage object types that this controller handles."""

    status_types: Optional[Tuple[str, ...]] = None
    """Which Vantage status types this controller handles, if any."""

    enhanced_log_status: bool = False
    """Should this controller subscribe to updates from the Enhanced Log."""

    enhanced_log_status_methods: Optional[Tuple[str, ...]] = None
    """Which status methods this controller handles from the Enhanced Log."""

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize instance."""
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscribed_to_event_stream = False
        self._subscriptions: List[EventSubscription[T]] = []
        self._id_subscriptions: Dict[int, List[EventSubscription[T]]] = {}

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

    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of an object."""

    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for an object."""

    @property
    def config_client(self) -> ConfigClient:
        """Return the config client instance."""
        return self._vantage.config_client

    @property
    def command_client(self) -> CommandClient:
        """Return the command client instance."""
        return self._vantage.command_client

    @property
    def event_stream(self) -> EventStream:
        """Return the event stream instance."""
        return self._vantage.event_stream

    async def initialize(self) -> None:
        """Populate objects and fetch their initial state."""

        # Save the previous set of object IDs, for comparison later
        prev_ids = set(self._items.keys())
        cur_ids = set()

        # Fetch all objects managed by this controller
        async for obj in get_objects(self.config_client, types=self.vantage_types):
            if obj.id not in prev_ids:
                # This is a new object, add it to the controller and notify subscribers
                self._items[obj.id] = obj
                self.emit(VantageEvent.OBJECT_ADDED, obj)

                # Fetch the initial state of the object
                await self.fetch_object_state(obj.id)
            else:
                # This is an existing object, check if any attributes have changed
                prev_obj = self._items[obj.id]
                attrs_changed = [
                    field.name
                    for field in fields(prev_obj)
                    if getattr(prev_obj, field.name) != getattr(obj, field.name)
                    and field.name != "mtime"
                ]

                # If any attributes changed, update the object and notify subscribers
                if attrs_changed:
                    self._items[obj.id] = obj
                    self.emit(
                        VantageEvent.OBJECT_UPDATED,
                        obj,
                        {"attrs_changed": attrs_changed},
                    )

            # Keep track of which objects we've seen
            cur_ids.add(obj.id)

        # Handle objects that were removed
        for vid in prev_ids - cur_ids:
            obj = self._items.pop(vid)
            self.emit(VantageEvent.OBJECT_REMOVED, obj)

        self._logger.info("%s initialized", self.__class__.__name__)

    async def subscribe(
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

        # Subscribe to the event stream if this is the first subscription
        if not self._subscribed_to_event_stream:
            await self._subscribe_to_event_stream()

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
        self, event_type: VantageEvent, obj: T, data: Optional[Dict[str, Any]] = None
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

    async def _subscribe_to_event_stream(self) -> None:
        # Ensure that the event stream is running
        await self.event_stream.start()

        # Re-fetch the full state of all objects after reconnecting
        self.event_stream.subscribe(self._handle_event, EventType.RECONNECTED)

        # Subscribe to "STATUS {type}" updates, if this controller cares about them
        if self.status_types:
            self.event_stream.subscribe_status(self._handle_event, self.status_types)

        # Subscribe to object status events from the "Enhanced Log"
        if self.enhanced_log_status:
            self.event_stream.subscribe_enhanced_log(
                self._handle_event, ("STATUS", "STATUSEX")
            )

        self._subscribed_to_event_stream = True
        self._logger.info("%s subscribed to event stream", self.__class__.__name__)

    async def _handle_event(self, event: Event) -> None:
        # Handle events from the event stream
        if event["type"] == EventType.STATUS:
            # Ignore events for objects that this controller doesn't manage
            if event["id"] not in self._items:
                return

            # Pass the event to the controller
            self.handle_object_update(event["id"], event["status_type"], event["args"])

        elif event["type"] == EventType.ENHANCED_LOG:
            # STATUS/STATUSEX logs can be tokenized the same as command responses
            id_str, method, *args = tokenize_response(event["log"])

            # Ignore events with methods that this controller doesn't care about
            if (
                self.enhanced_log_status_methods
                and method not in self.enhanced_log_status_methods
            ):
                return

            # Ignore events for objects that this controller doesn't manage
            vid = int(id_str)
            if vid not in self._items:
                return

            # Pass the event to the controller
            self.handle_object_update(vid, method, args)

        elif event["type"] == EventType.RECONNECTED:
            # Fetch the full state of all objects after reconnecting
            await asyncio.gather(
                *[self.fetch_object_state(obj.id) for obj in self._items.values()]
            )
