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
    Literal,
    Optional,
    Sequence,
    Set,
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

# Type for state updates
State = Optional[Dict[str, Any]]


class BaseController(QuerySet[T]):
    """Base controller for Vantage objects."""

    vantage_types: Tuple[str, ...]
    """The Vantage object types that this controller handles."""

    status_types: Optional[Tuple[str, ...]] = None
    """Which Vantage 'STATUS' types this controller handles, if any."""

    enhanced_log_status_methods: Optional[Union[Tuple[str, ...], Literal["*"]]] = None
    """Which status methods this controller handles from the Enhanced Log."""

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize a controller.

        Args:
            vantage: The Vantage instance.
            init_callback: A callback to call when the controller is initialized.
        """
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscribed_to_state_changes = False
        self._subscriptions: List[EventSubscription[T]] = []
        self._id_subscriptions: Dict[int, List[EventSubscription[T]]] = {}
        self._initialized = False

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
        return bool(self.status_types or self.enhanced_log_status_methods)

    @property
    def known_ids(self) -> Set[int]:
        """Return a set of all known object IDs."""
        return set(self._items.keys())

    async def fetch_object_state(self, _vid: int) -> State:
        """Fetch the full state of an object, should be overridden by subclasses."""
        return None

    def parse_object_update(
        self, _vid: int, _status: str, _args: Sequence[str]
    ) -> State:
        """Parse updates from the event stream for an object, should be overridden by subclasses."""
        return None

    async def initialize(self, fetch_state: bool = True) -> None:
        """Populate objects and fetch their initial state."""
        prev_ids = set(self._items.keys())
        cur_ids = set()

        # Fetch all objects managed by this controller
        async for obj in get_objects(self.config_client, types=self.vantage_types):
            if obj.id not in prev_ids:
                # This is a new object, add it to the controller
                self._items[obj.id] = obj

                # Fetch the state of the object
                if self.stateful and fetch_state:
                    self._set_state(obj, await self.fetch_object_state(obj.id))

                # Notify subscribers that a new object was added
                self.emit(VantageEvent.OBJECT_ADDED, obj)
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
                    for attr in attrs_changed:
                        try:
                            setattr(prev_obj, attr, getattr(obj, attr))
                        except AttributeError:
                            self._logger.warning("Object has no attribute '%s'", attr)

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
            self.emit(VantageEvent.OBJECT_DELETED, obj)

        # Subscribe to state changes for objects managed by this controller
        if fetch_state:
            await self.subscribe_to_state_changes()

        # Mark the controller as initialized
        if not self._initialized:
            self._initialized = True
            self._logger.info("%s initialized", self.__class__.__name__)
        else:
            self._logger.info("%s reinitialized", self.__class__.__name__)

    async def fetch_full_state(self) -> None:
        """Fetch the full state of all objects managed by this controller."""
        if not self.stateful:
            return

        for obj in self._items.values():
            self._update_state(obj.id, await self.fetch_object_state(obj.id))

        self._logger.info("%s fetched state", self.__class__.__name__)

    async def subscribe_to_state_changes(self) -> None:
        """Subscribe to state changes for objects managed by this controller."""
        if self._subscribed_to_state_changes or not self.stateful:
            return

        # Ensure that the event stream is running
        await self.event_stream.start()

        # Subscribe to "STATUS {type}" updates, if this controller cares about them
        if self.status_types:
            self.event_stream.subscribe_status(self._handle_event, self.status_types)

        # Subscribe to object status events from the "Enhanced Log"
        if self.enhanced_log_status_methods:
            self.event_stream.subscribe_enhanced_log(
                self._handle_event, ("STATUS", "STATUSEX")
            )

        self._subscribed_to_state_changes = True
        self._logger.info("%s subscribed to state changes", self.__class__.__name__)

    def subscribe(
        self,
        callback: EventCallback[T],
        id_filter: Union[int, Tuple[int], None] = None,
        event_filter: Union[VantageEvent, Tuple[VantageEvent, ...], None] = None,
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

    def _set_state(self, obj: T, state: State) -> None:
        # Set the state properties of an object.
        if state is None:
            return

        for key, value in state.items():
            try:
                setattr(obj, key, value)
            except AttributeError:
                self._logger.warning("Object '%d' has no attribute '%s'", obj.id, key)

    def _update_state(self, vid: int, state: State) -> None:
        """Update the state of an object and notify subscribers if it changed."""
        if state is None:
            return

        # Ignore updates for objects that this controller doesn't manage
        if (obj := self._items.get(vid)) is None:
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

    async def _handle_event(self, event: Event) -> None:
        # Handle events from the event stream
        # pylint: disable=assignment-from-none
        if event["type"] == EventType.STATUS:
            # Ignore events for objects that this controller doesn't manage
            if event["id"] not in self._items:
                return

            # Pass the event to the controller
            state = self.parse_object_update(
                event["id"], event["status_type"], event["args"]
            )
            self._update_state(event["id"], state)

        elif event["type"] == EventType.ENHANCED_LOG:
            # STATUS/STATUSEX logs can be tokenized the same as command responses
            id_str, method, *args = tokenize_response(event["log"])

            # Ignore events with methods that this controller doesn't care about
            if not (
                self.enhanced_log_status_methods
                and (
                    self.enhanced_log_status_methods == "*"
                    or method in self.enhanced_log_status_methods
                )
            ):
                return

            # Ignore events for objects that this controller doesn't manage
            vid = int(id_str)
            if vid not in self._items:
                return

            # Pass the event to the controller
            state = self.parse_object_update(vid, method, args)
            self._update_state(vid, state)

    async def _lazy_initialize(self) -> None:
        # Initialize the controller if it isn't already initialized
        if not self._initialized:
            await self.initialize()
