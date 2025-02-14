import asyncio
from collections.abc import Callable
from dataclasses import fields
from enum import Enum
from typing import TYPE_CHECKING, TypeVar, cast

from aiovantage._logger import logger
from aiovantage.command_client import Converter
from aiovantage.config_client import ConfigurationInterface
from aiovantage.events import (
    EnhancedLogReceived,
    EventDispatcher,
    ObjectAdded,
    ObjectDeleted,
    ObjectUpdated,
    Reconnected,
    StatusReceived,
)
from aiovantage.objects import SystemObject

from .query import QuerySet

if TYPE_CHECKING:
    from aiovantage import Vantage

T = TypeVar("T", bound=SystemObject)


class StatusType(Enum):
    """The type of status that the controller is using for state monitoring."""

    OBJECT = 1
    """Object status events from the Enhanced Log."""

    CATEGORY = 2
    """Category status events, eg: S:LOAD, S:BLIND, etc."""


class Controller(QuerySet[T], EventDispatcher):
    """Base controller for managing collections of Vantage objects."""

    vantage_types: tuple[str, ...]
    """The Vantage object types that this controller will fetch."""

    force_category_status: bool = False
    """Whether to force the controller to handle 'STATUS' categories."""

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize a controller.

        Args:
            vantage: The Vantage instance.
        """
        self._vantage = vantage
        self._objects: dict[int, T] = {}
        self._initialized = False
        self._status_type: StatusType | None = None
        self._status_unsubs: list[Callable[[], None]] = []
        self._lock = asyncio.Lock()

        QuerySet[T].__init__(self, self._objects, self._lazy_initialize)
        EventDispatcher.__init__(self)

    def __getitem__(self, vid: int) -> T:
        """Return the object with the given Vantage ID."""
        return self._objects[vid]

    def __contains__(self, vid: int) -> bool:
        """Return True if the object with the given Vantage ID exists."""
        return vid in self._objects

    @property
    def status_type(self) -> StatusType | None:
        """Return the type of status event that the controller is monitoring."""
        return self._status_type

    async def initialize(
        self, *, fetch_state: bool = True, enable_state_monitoring: bool = True
    ) -> None:
        """Populate the controller, and optionally fetch object state.

        Args:
            fetch_state: Whether to fetch the state properties of objects.
            enable_state_monitoring: Whether to monitor for state changes on objects.
        """
        # Prevent concurrent controller initialization from multiple tasks, since we
        # are batch-modifying the _items dict.
        async with self._lock:
            prev_ids = set(self._objects.keys())
            cur_ids: set[int] = set()

            # Fetch all objects managed by this controller
            async for obj in ConfigurationInterface.get_objects(
                self._vantage.config_client, *self.vantage_types, as_type=SystemObject
            ):
                obj = cast(T, obj)

                if obj.vid in prev_ids:
                    # This is an existing object.
                    existing_obj = self._objects[obj.vid]

                    # Check if any attributes have changed and update them
                    attrs_changed: list[str] = []
                    for f in fields(type(obj)):
                        if hasattr(existing_obj, f.name):
                            new_value = getattr(obj, f.name)
                            if getattr(existing_obj, f.name) != new_value:
                                setattr(existing_obj, f.name, new_value)
                                attrs_changed.append(f.name)

                    # Notify subscribers if any attributes changed
                    if attrs_changed:
                        self.emit(ObjectUpdated(existing_obj, attrs_changed))
                else:
                    # This is a new object.

                    # Attach the command client to the object
                    obj.command_client = self._vantage.command_client

                    # Add it to the controller and notify subscribers
                    self._objects[obj.vid] = obj
                    self.emit(ObjectAdded(obj))

                # Keep track of which objects we've seen
                cur_ids.add(obj.vid)

            # Handle objects that were removed
            for vid in prev_ids - cur_ids:
                obj = self._objects.pop(vid)
                self.emit(ObjectDeleted(obj))

        logger.info(
            "%s populated (%d objects)", type(self).__name__, len(self._objects)
        )

        # Mark the controller as initialized
        if not self._initialized:
            self._initialized = True

        # Fetch state and subscribe to state changes if requested
        if self._objects:
            if fetch_state:
                await self.fetch_state()

            if enable_state_monitoring:
                await self.enable_state_monitoring()

    async def fetch_state(self) -> None:
        """Fetch the state properties of all objects managed by this controller."""
        for obj in self._objects.values():
            # Fetch state, and notify subscribers if any attributes changed
            attrs_changed = await obj.fetch_state()
            if attrs_changed:
                self.emit(ObjectUpdated(obj, attrs_changed))

        logger.info("%s fetched state", type(self).__name__)

    async def enable_state_monitoring(self) -> None:
        """Monitor for state changes on objects managed by this controller."""
        if self._status_type is not None:
            return

        # Start the event stream if it isn't already running
        event_conn = await self._vantage.event_stream.start()

        # When available, we'll use "object" status events (subscribed via
        # the Enhanced Log) because they support a richer set of status properties.
        # If these are not supported—either due to older firmware, or if the
        # controller explicitly requesting category statuses, we'll fall back to
        # "category" status events.
        if event_conn.supports_enhanced_log and not self.force_category_status:
            # Subscribe to "object status" events from the Enhanced Log.
            status_unsub = self._vantage.event_stream.subscribe_enhanced_log(
                self._handle_enhanced_log_event, "STATUS", "STATUSEX"
            )

            self._status_type = StatusType.OBJECT
        else:
            # Subscribe to "STATUS {category}" updates
            status_unsub = self._vantage.event_stream.subscribe_status(
                self._handle_status_event
            )

            self._status_type = StatusType.CATEGORY

        # Subscribe to reconnect events from the event stream
        reconnect_unsub = self._vantage.event_stream.subscribe(
            Reconnected, self._handle_reconnect_event
        )

        # Keep track of the subscriptions so we can unsubscribe later
        self._status_unsubs.extend([status_unsub, reconnect_unsub])

        logger.info("%s subscribed to state changes", type(self).__name__)

    async def disable_state_monitoring(self) -> None:
        """Stop monitoring for state changes on objects managed by this controller."""
        if self._status_type is None:
            return

        # Unsubscribe status and reconnect events
        while self._status_unsubs:
            unsub = self._status_unsubs.pop()
            unsub()

        self._status_type = None

        logger.info("%s unsubscribed from state changes", type(self).__name__)

    def _handle_status_event(self, event: StatusReceived) -> None:
        # Look up the object that this event is for
        obj = self._objects.get(event.vid)
        if obj is None:
            return

        # Handle the event
        if event.category == "STATUS":
            # Handle "object interface" status events of the form:
            # -> S:STATUS <vid> <method> <result> <arg1> <arg2> ...
            attrs_changed = obj.handle_object_status(*event.args)
        else:
            # Handle "category" status events, eg: S:LOAD, S:BLIND, etc
            # -> S:LOAD <vid> <arg1> <arg2> ...
            attrs_changed = obj.handle_category_status(event.category, *event.args)

        # Notify subscribers if any attributes changed
        if attrs_changed:
            self.emit(ObjectUpdated(obj, attrs_changed))

    def _handle_enhanced_log_event(self, event: EnhancedLogReceived) -> None:
        # Tokenize STATUS/STATUSEX logs from the enhanced log.
        # These are "object interface" status messages, of the form:
        # -> EL: <vid> <method> <result> <arg1> <arg2> ...
        vid_str, method, result, *args = Converter.tokenize(event.log)

        # Pass the event to the controller, if this object is managed by it
        obj = self._objects.get(int(vid_str))
        if obj is None:
            return

        # Handle the event, and notify subscribers if any attributes changed
        attrs_changed = obj.handle_object_status(method, result, *args)
        if attrs_changed:
            self.emit(ObjectUpdated(obj, attrs_changed))

    def _handle_reconnect_event(self, event: Reconnected) -> None:
        # Fetch latest state if we've been disconnected
        asyncio.create_task(self.fetch_state())

    async def _lazy_initialize(self) -> None:
        # Initialize the controller if it isn't already initialized
        if not self._initialized:
            await self.initialize()
