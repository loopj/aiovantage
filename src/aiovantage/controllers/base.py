"""Base controller for Vantage objects."""

import asyncio
import logging
from collections.abc import Callable, Iterable
from dataclasses import fields
from inspect import iscoroutinefunction
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from aiovantage.command_client import CommandClient, Event, EventStream, EventType
from aiovantage.command_client.utils import tokenize_response
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

    vantage_types: tuple[type[SystemObject], ...]
    """The Vantage object types that this controller handles."""

    status_types: tuple[str, ...] | None = None
    """Which Vantage 'STATUS' types this controller handles, if any."""

    interface_status_types: tuple[str, ...] | Literal["*"] | None = None
    """Which object interface status messages this controller handles, if any."""

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

        QuerySet.__init__(self, self._items, self._lazy_initialize)

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

    @property
    def stateful(self) -> bool:
        """Return True if this controller manages stateful objects."""
        return bool(self.status_types or self.interface_status_types)

    @property
    def known_ids(self) -> set[int]:
        """Return a set of all known object IDs."""
        return set(self._items.keys())

    async def fetch_object_state(self, obj: T) -> None:
        """Fetch the full state of an object.

        Should be overridden by subclasses that manage stateful objects.
        """
        return

    def handle_status(self, _vid: int, _status: str, *_args: str) -> None:
        """Handle simple status messages from the event stream.

        Should be overridden by subclasses that manage stateful objects using
        "STATUS {type}" messages.
        """
        return

    def handle_interface_status(
        self, _vid: int, _method: str, _result: str, *_args: str
    ) -> None:
        """Handle object interface status messages from the event stream.

        Should be overridden by subclasses that manage stateful objects using object
        interface status messages from "ADDSTATUS {vid}" or "ELLOG STATUS" events.
        """
        return

    async def initialize(self, fetch_state: bool = True) -> None:
        """Populate the controller, and optionally fetch initial state.

        Args:
            fetch_state: Whether to also fetch the state of each object.
        """
        # Prevent concurrent controller initialization from multiple tasks, since we
        # are batch-modifying the _items dict.
        async with self._lock:
            prev_ids = set(self._items.keys())
            cur_ids = set()

            # Fetch all objects managed by this controller
            element_names = tuple(cls.get_element_name() for cls in self.vantage_types)
            async for obj in get_objects(self.config_client, types=element_names):
                obj._command_client = self.command_client

                if obj.vid in prev_ids:
                    # This is an existing object.
                    # Update any attributes that have changed and notify subscribers.
                    # Ignore the m_time attribute, and any state attributes.
                    # TODO: Check if interface state fields even show up here now
                    self.update_state(
                        obj.vid,
                        {
                            field.name: getattr(obj, field.name)
                            for field in fields(type(obj))
                            if field.name != "m_time"
                            and field.metadata.get("type") != "Ignore"
                        },
                    )
                else:
                    # This is a new object.
                    # Add it to the controller and notify subscribers
                    self._items[obj.vid] = obj
                    self.emit(VantageEvent.OBJECT_ADDED, obj)

                    # Fetch the state of stateful objects
                    if self.stateful and fetch_state:
                        await self.fetch_object_state(obj)

                # Keep track of which objects we've seen
                cur_ids.add(obj.vid)

            # Handle objects that were removed
            for vid in prev_ids - cur_ids:
                obj = self._items.pop(vid)
                self.emit(VantageEvent.OBJECT_DELETED, obj)

        # Subscribe to state changes for objects managed by this controller
        if fetch_state and len(self._items) > 0:
            await self.subscribe_to_state_changes()

        # Mark the controller as initialized
        if not self._initialized:
            self._initialized = True

        self._logger.info(
            "%s initialized (%d objects)", type(self).__name__, len(self._items)
        )

    async def fetch_full_state(self) -> None:
        """Fetch the full state of all objects managed by this controller."""
        if not self.stateful:
            return

        for obj in self._items.values():
            await self.fetch_object_state(obj)

        self._logger.info("%s fetched state", type(self).__name__)

    async def subscribe_to_state_changes(self) -> None:
        """Subscribe to state changes for objects managed by this controller."""
        if self._subscribed_to_state_changes or not self.stateful:
            return

        # Ensure that the event stream is running
        await self.event_stream.start()

        # Subscribe to "STATUS {type}" updates, if this controller cares about them.
        if self.status_types:
            self.event_stream.subscribe_status(self._handle_event, self.status_types)

        # Some state changes are only available from "object" status events.
        # These can be subscribed to by using "STATUSADD {vid}" or "ELLOG STATUS".
        if self.interface_status_types:
            # Subscribe to "object status" events from the Enhanced Log.
            self.event_stream.subscribe_enhanced_log(
                self._handle_event, ("STATUS", "STATUSEX")
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
        subscribers = self._subscriptions + self._id_subscriptions.get(obj.vid, [])
        for callback, event_filter in subscribers:
            if event_filter is not None and event_type not in event_filter:
                continue

            if iscoroutinefunction(callback):
                asyncio.create_task(callback(event_type, obj, data))  # noqa: RUF006
            else:
                callback(event_type, obj, data)

    def update_state(self, vid: int, attrs: dict[str, Any]) -> None:
        """Update the attributes of an object and notify subscribers of changes."""
        # Ignore updates for objects that this controller doesn't manage
        if (obj := self._items.get(vid)) is None:
            return

        # Check if any state attributes changed and update them
        attrs_changed = []
        for key, value in attrs.items():
            try:
                if getattr(obj, key) != value:
                    setattr(obj, key, value)
                    attrs_changed.append(key)
            except AttributeError:
                self._logger.warning("Object '%d' has no attribute '%s'", obj.vid, key)

        # Notify subscribers if any attributes changed
        if len(attrs_changed) > 0:
            self.emit(
                VantageEvent.OBJECT_UPDATED,
                obj,
                {"attrs_changed": attrs_changed},
            )

    async def _handle_event(self, event: Event) -> None:
        # Handle events from the event stream
        if event["type"] == EventType.STATUS:
            # Ignore events for objects that this controller doesn't manage
            if event["id"] not in self._items:
                return

            if event["status_type"] == "STATUS":
                # Handle "object interface" status events of the form:
                # -> S:STATUS <id> <method> <result> <arg1> <arg2> ...
                method, result, *args = event["args"]
                self.handle_interface_status(event["id"], method, result, *args)
            else:
                # Handle "category" status events, eg: S:LOAD, S:BLIND, etc
                self.handle_status(event["id"], event["status_type"], *event["args"])

        elif event["type"] == EventType.ENHANCED_LOG:
            # We only ever subscribe to STATUS/STATUSEX logs from the enhanced log.
            # These are "object interface" status messages, of the form:
            #   EL: <id> <method> <result> <arg1> <arg2> ...
            vid_str, method, result, *args = tokenize_response(event["log"])
            vid = int(vid_str)

            # Ignore events for objects that this controller doesn't manage
            if vid not in self._items:
                return

            # Pass the event to the controller
            self.handle_interface_status(vid, method, result, *args)

    async def _lazy_initialize(self) -> None:
        # Initialize the controller if it isn't already initialized
        if not self._initialized:
            await self.initialize()
