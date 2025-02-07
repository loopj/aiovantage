"""Base controller for Vantage objects."""

import asyncio
from collections.abc import Callable, Iterable
from dataclasses import fields
from inspect import iscoroutinefunction
from typing import TYPE_CHECKING, Any, TypeVar, cast

from aiovantage._logger import logger
from aiovantage.command_client import Converter, Event, EventType
from aiovantage.config_client import ConfigurationInterface
from aiovantage.events import EventCallback, VantageEvent
from aiovantage.objects import SystemObject
from aiovantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage import Vantage

T = TypeVar("T", bound=SystemObject)


# Types for state and subscriptions
EventSubscription = tuple[EventCallback[T], Iterable[VantageEvent] | None]


class BaseController(QuerySet[T]):
    """Base controller for managing collections of Vantage objects."""

    vantage_types: tuple[str, ...]
    """The Vantage object types that this controller will fetch."""

    category_status: bool = False
    """Whether to force the controller to handle 'STATUS' categories."""

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize a controller.

        Args:
            vantage: The Vantage instance.
        """
        self._vantage = vantage
        self._items: dict[int, T] = {}
        self._subscribed_to_state_changes = False
        self._subscriptions: list[EventSubscription[T]] = []
        self._id_subscriptions: dict[int, list[EventSubscription[T]]] = {}
        self._initialized = False
        self._lock = asyncio.Lock()

        super().__init__(self._items, self._lazy_initialize)

    def __getitem__(self, vid: int) -> T:
        """Return the object with the given Vantage ID."""
        return self._items[vid]

    def __contains__(self, vid: int) -> bool:
        """Return True if the object with the given Vantage ID exists."""
        return vid in self._items

    @property
    def initialized(self) -> bool:
        """Return True if this controller has been initialized."""
        return self._initialized

    async def initialize(
        self, *, fetch_state: bool = True, monitor_state: bool = True
    ) -> None:
        """Populate the controller, and optionally fetch object state.

        Args:
            fetch_state: Whether to fetch the state of stateful objects.
            monitor_state: Whether to keep the state of stateful objects up-to-date.
        """
        # Prevent concurrent controller initialization from multiple tasks, since we
        # are batch-modifying the _items dict.
        async with self._lock:
            prev_ids = set(self._items.keys())
            cur_ids: set[int] = set()

            # Fetch all objects managed by this controller
            async for obj in ConfigurationInterface.get_objects(
                self._vantage.config_client, *self.vantage_types, as_type=SystemObject
            ):
                obj = cast(T, obj)

                if obj.vid in prev_ids:
                    # This is an existing object.
                    existing_obj = self._items[obj.vid]

                    # Check if any attributes have changed and update them
                    changed: list[str] = []
                    for f in fields(type(obj)):
                        if hasattr(existing_obj, f.name):
                            new_value = getattr(obj, f.name)
                            if getattr(existing_obj, f.name) != new_value:
                                setattr(existing_obj, f.name, new_value)
                                changed.append(f.name)

                    # Notify subscribers if any attributes changed
                    if changed:
                        self._object_updated(existing_obj, *changed)
                else:
                    # This is a new object.

                    # Attach the command client to the object
                    obj.command_client = self._vantage.command_client

                    # Add it to the controller and notify subscribers
                    self._items[obj.vid] = obj
                    self._emit(VantageEvent.OBJECT_ADDED, obj)

                # Keep track of which objects we've seen
                cur_ids.add(obj.vid)

            # Handle objects that were removed
            for vid in prev_ids - cur_ids:
                obj = self._items.pop(vid)
                self._emit(VantageEvent.OBJECT_DELETED, obj)

        logger.info("%s populated (%d objects)", type(self).__name__, len(self._items))

        # Mark the controller as initialized
        if not self._initialized:
            self._initialized = True

        # Fetch state and subscribe to state changes if requested
        if self._items:
            if fetch_state:
                await self.fetch_state()

            if monitor_state:
                await self.monitor_state()

    async def fetch_state(self) -> None:
        """Fetch the state properties of all objects managed by this controller."""
        for obj in self._items.values():
            # Fetch all state properties defined by the object's interface(s)
            props_changed = await obj.fetch_state()

            # Notify subscribers if any attributes changed
            if props_changed:
                self._object_updated(obj, *props_changed)

        logger.info("%s fetched state", type(self).__name__)

    async def monitor_state(self) -> None:
        """Monitor for state changes for objects managed by this controller."""
        if self._subscribed_to_state_changes:
            return

        # Start the event stream if it isn't already running
        event_conn = await self._vantage.event_stream.start()

        # When available, we'll use "object" status events (subscribed via
        # the Enhanced Log) because they support a richer set of status properties.
        # If these are not supported—either due to older firmware, or if the
        # controller explicitly requesting category statuses, we'll fall back to
        # "category" status events.
        if event_conn.supports_enhanced_log and not self.category_status:
            # Subscribe to "object status" events from the Enhanced Log.
            self._vantage.event_stream.subscribe_enhanced_log(
                self._handle_enhanced_log_event, "STATUS", "STATUSEX"
            )
        else:
            # Subscribe to "STATUS {category}" updates
            self._vantage.event_stream.subscribe_status(self._handle_status_event)

        self._subscribed_to_state_changes = True
        logger.info("%s subscribed to state changes", type(self).__name__)

    def subscribe(
        self,
        callback: EventCallback[T],
        id_filter: int | Iterable[int] | None = None,
        event_filter: VantageEvent | Iterable[VantageEvent] | None = None,
    ) -> Callable[[], None]:
        """Subscribe to status changes for objects managed by this controller.

        Args:
            callback: The callback to call when an object changes.
            id_filter: The Vantage IDs to subscribe to, all objects if None.
            event_filter: The event types to subscribe to, all events if None.

        Returns:
            A function to unsubscribe from the callback.
        """
        # Handle single ID filter or single event filter
        if isinstance(id_filter, int):
            id_filter = (id_filter,)

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

    def _emit(
        self, event_type: VantageEvent, obj: T, data: dict[str, Any] | None = None
    ) -> None:
        # Emit an event to subscribers of this controller.
        if data is None:
            data = {}

        # Grab a list of subscribers that care about this object
        subscribers = self._subscriptions + self._id_subscriptions.get(obj.vid, [])
        for callback, event_filter in subscribers:
            if event_filter is not None and event_type not in event_filter:
                continue

            if iscoroutinefunction(callback):
                asyncio.create_task(callback(event_type, obj, data))  # noqa: RUF006
            else:
                callback(event_type, obj, data)

    def _object_updated(self, obj: T, *attrs_changed: str) -> None:
        # Notify subscribers that an object has been updated
        self._emit(VantageEvent.OBJECT_UPDATED, obj, {"attrs_changed": attrs_changed})

    async def _handle_status_event(self, event: Event) -> None:
        if event["type"] != EventType.STATUS:
            return

        # Look up the object that this event is for
        obj = self._items.get(event["vid"])
        if obj is None:
            return

        # Handle the event
        if event["category"] == "STATUS":
            # Handle "object interface" status events of the form:
            # -> S:STATUS <vid> <method> <result> <arg1> <arg2> ...
            method, result, *args = event["args"]
            updated = obj.handle_object_status(method, result, *args)
        else:
            # Handle "category" status events, eg: S:LOAD, S:BLIND, etc
            # -> S:LOAD <vid> <arg1> <arg2> ...
            category, *args = event["category"], *event["args"]
            updated = obj.handle_category_status(category, *args)

        # Notify subscribers if any attributes changed
        if updated:
            self._object_updated(obj, updated)

    async def _handle_enhanced_log_event(self, event: Event) -> None:
        if event["type"] != EventType.ENHANCED_LOG:
            return

        # Tokenize STATUS/STATUSEX logs from the enhanced log.
        # These are "object interface" status messages, of the form:
        # -> EL: <vid> <method> <result> <arg1> <arg2> ...
        vid_str, method, result, *args = Converter.tokenize(event["log"])
        vid = int(vid_str)

        # Pass the event to the controller, if this object is managed by it
        obj = self._items.get(vid)
        if obj is None:
            return

        # Handle the event
        updated = obj.handle_object_status(method, result, *args)

        # Notify subscribers if any attributes changed
        if updated:
            self._object_updated(obj, updated)

    async def _lazy_initialize(self) -> None:
        # Initialize the controller if it isn't already initialized
        if not self._initialized:
            await self.initialize()
