"""Base controller for Vantage objects."""

import asyncio
import logging
from collections.abc import Callable, Iterable
from dataclasses import fields
from inspect import iscoroutinefunction
from typing import TYPE_CHECKING, Any, TypeVar, cast

from aiovantage.command_client import CommandClient, Event, EventStream, EventType
from aiovantage.command_client.types import tokenize_response
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.requests import get_objects
from aiovantage.events import EventCallback, VantageEvent
from aiovantage.objects import SystemObject
from aiovantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage import Vantage

T = TypeVar("T", bound=SystemObject)


# Types for state and subscriptions
EventSubscription = tuple[EventCallback[T], Iterable[VantageEvent] | None]


class BaseController(QuerySet[T]):
    """Base controller for Vantage objects."""

    vantage_types: tuple[str, ...]
    """The Vantage object types that this controller handles."""

    status_categories: tuple[str, ...] | None = None
    """Which Vantage 'STATUS' categories this controller handles, if any."""

    force_category_status: bool = False
    """Whether to force the controller to handle 'STATUS' categories."""

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize a controller.

        Args:
            vantage: The Vantage instance.
        """
        self._vantage = vantage
        self._items: dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscribed_to_state_changes = False
        self._subscriptions: list[EventSubscription[T]] = []
        self._id_subscriptions: dict[int, list[EventSubscription[T]]] = {}
        self._initialized = False
        self._lock = asyncio.Lock()

        super().__init__(self._items, self._lazy_initialize)

        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initialization hook for subclasses."""

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

    @property
    def event_stream(self) -> EventStream:
        """Return the event stream instance."""
        return self._vantage.event_stream

    @property
    def initialized(self) -> bool:
        """Return True if this controller has been initialized."""
        return self._initialized

    async def fetch_object_state(self, obj: T) -> None:
        """Fetch the full state of an object.

        Args:
            obj: The object to fetch the state of.
        """
        # Fetch all state properties defined by the object's interface(s)
        props_changed = await obj.fetch_state()

        # Notify subscribers if any attributes changed
        self.object_updated(obj, props_changed)

    def handle_category_status(self, obj: T, status: str, *args: str) -> None:
        """Handle "category" status messages from the event stream.

        Args:
            obj: The object that the status message is for.
            status: The status category.
            args: The arguments to the status message.
        """
        updated_properties = obj.handle_category_status(status, *args)
        if updated_properties:
            self.object_updated(obj, [updated_properties])

    def handle_object_status(
        self, obj: T, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream.

        Args:
            obj: The object that the status message is for.
            method: The method that was called.
            result: The result of the method call.
            args: The arguments to the method call.
        """
        updated_properties = obj.handle_object_status(method, result, *args)
        if updated_properties:
            self.object_updated(obj, [updated_properties])

    async def initialize(
        self,
        *,
        fetch_state: bool = True,
        subscribe_state: bool = True,
        enhanced_log: bool = True,
    ) -> None:
        """Populate the controller, and optionally fetch object state.

        Args:
            fetch_state: Whether to fetch the state of stateful objects.
            subscribe_state: Whether to keep the state of stateful objects up-to-date.
            enhanced_log: Whether to use the Enhanced Log for state updates.
        """
        # Prevent concurrent controller initialization from multiple tasks, since we
        # are batch-modifying the _items dict.
        async with self._lock:
            prev_ids = set(self._items.keys())
            cur_ids: set[int] = set()

            # Fetch all objects managed by this controller
            async for obj in get_objects(self.config_client, *self.vantage_types):
                obj = cast(T, obj)

                if obj.id in prev_ids:
                    # This is an existing object.
                    # Update any attributes that have changed and notify subscribers.
                    # Ignore any state attributes.
                    self.update_state(
                        obj,
                        {
                            field.name: getattr(obj, field.name)
                            for field in fields(type(obj))
                        },
                    )
                else:
                    # This is a new object.
                    # Attach the command client to the object
                    obj.command_client = self.command_client

                    # Add it to the controller and notify subscribers
                    self._items[obj.id] = obj
                    self.emit(VantageEvent.OBJECT_ADDED, obj)

                    # Fetch the state of stateful objects
                    if fetch_state:
                        await self.fetch_object_state(obj)

                # Keep track of which objects we've seen
                cur_ids.add(obj.id)

            # Handle objects that were removed
            for vid in prev_ids - cur_ids:
                obj = self._items.pop(vid)
                self.emit(VantageEvent.OBJECT_DELETED, obj)

        # Subscribe to state changes for objects managed by this controller
        if subscribe_state:
            await self.subscribe_to_state_changes(enhanced_log=enhanced_log)

        # Mark the controller as initialized
        if not self._initialized:
            self._initialized = True

        self._logger.info(
            "%s initialized (%d objects)", type(self).__name__, len(self._items)
        )

    async def fetch_full_state(self) -> None:
        """Fetch the full state of all objects managed by this controller."""
        for obj in self._items.values():
            await self.fetch_object_state(obj)

        self._logger.info("%s fetched state", type(self).__name__)

    async def subscribe_to_state_changes(self, *, enhanced_log: bool = True) -> None:
        """Subscribe to state changes for objects managed by this controller.

        Args:
            enhanced_log: Whether to use the Enhanced Log for state updates.
        """
        if self._subscribed_to_state_changes:
            return

        # Ensure that the event stream is running
        await self.event_stream.start()

        # Subscribe to "STATUS {category}" updates
        # We should only do this if "object" status is not supported, or this
        # controller explicitly requests to handle "category" status messages.
        if not enhanced_log or self.force_category_status:
            if self.status_categories:
                self.event_stream.subscribe_status(
                    self._handle_event, *self.status_categories
                )

        # Some state changes are only available from "object" status events.
        # These can be subscribed to by using "STATUSADD {vid}" or "ELLOG STATUS".
        if enhanced_log:
            # Subscribe to "object status" events from the Enhanced Log.
            self.event_stream.subscribe_enhanced_log(
                self._handle_event, "STATUS", "STATUSEX"
            )

        self._subscribed_to_state_changes = True
        self._logger.info("%s subscribed to state changes", type(self).__name__)

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

    def emit(
        self, event_type: VantageEvent, obj: T, data: dict[str, Any] | None = None
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

    def object_updated(self, obj: T, attrs_changed: list[str]) -> None:
        """Notify subscribers that an object has been updated."""
        self.emit(
            VantageEvent.OBJECT_UPDATED,
            obj,
            {"attrs_changed": attrs_changed},
        )

    def update_state(self, obj: T, attrs: dict[str, Any]) -> None:
        """Update the attributes of an object and notify subscribers of changes."""
        # Check if any state attributes changed and update them
        attrs_changed: list[str] = []
        for key, value in attrs.items():
            try:
                if getattr(obj, key) != value:
                    setattr(obj, key, value)
                    attrs_changed.append(key)
            except AttributeError:
                self._logger.warning("Object '%d' has no attribute '%s'", obj.id, key)

        # Notify subscribers if any attributes changed
        if len(attrs_changed) > 0:
            self.object_updated(obj, attrs_changed)

    async def _handle_event(self, event: Event) -> None:
        # Handle events from the event stream
        if event["type"] == EventType.STATUS:
            # Look up the object that this event is for
            if obj := self._items.get(event["id"]):
                if event["category"] == "STATUS":
                    # Handle "object interface" status events of the form:
                    # -> S:STATUS <id> <method> <result> <arg1> <arg2> ...
                    method, result, *args = event["args"]
                    self.handle_object_status(obj, method, result, *args)
                else:
                    # Handle "category" status events, eg: S:LOAD, S:BLIND, etc
                    self.handle_category_status(obj, event["category"], *event["args"])

        elif event["type"] == EventType.ENHANCED_LOG:
            # We only ever subscribe to STATUS/STATUSEX logs from the enhanced log.
            # These are "object interface" status messages, of the form:
            #   EL: <id> <method> <result> <arg1> <arg2> ...
            vid_str, method, result, *args = tokenize_response(event["log"])
            vid = int(vid_str)

            # Pass the event to the controller, if this object is managed by it
            if obj := self._items.get(vid):
                self.handle_object_status(obj, method, result, *args)

    async def _lazy_initialize(self) -> None:
        # Initialize the controller if it isn't already initialized
        if not self._initialized:
            await self.initialize()
