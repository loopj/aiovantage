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
from aiovantage.command_client.helpers import tokenize_response
from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects_by_type
from aiovantage.config_client.objects import SystemObject
from aiovantage.events import VantageEvent
from aiovantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage import Vantage

T = TypeVar("T", bound="SystemObject")


# Types for callbacks for event subscriptions
EventCallback = Callable[[VantageEvent, T, Dict[str, Any]], None]
EventSubscription = Tuple[EventCallback[T], Optional[Iterable[VantageEvent]]]


class BaseController(QuerySet[T]):
    # The Vantage object types that this controller handles
    vantage_types: Tuple[str, ...]

    def __init__(self, vantage: "Vantage") -> None:
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscriptions: List[EventSubscription[T]] = []
        self._id_subscriptions: Dict[int, List[EventSubscription[T]]] = {}
        self._initialized = False

        QuerySet.__init__(self, self._items, self.initialize)

    def __getitem__(self, id: int) -> T:
        return self._items[id]

    def __contains__(self, id: int) -> bool:
        return id in self._items

    @property
    def config_client(self) -> ConfigClient:
        return self._vantage._config_client

    @property
    def command_client(self) -> CommandClient:
        return self._vantage._command_client

    async def initialize(self) -> None:
        """
        Initialize a stateless controller by populating the objects it manages.
        """

        # TODO: Allow reinitalization

        if self._initialized:
            return

        await self.fetch_objects()

        self._initialized = True

    async def fetch_objects(self) -> None:
        """
        Fetch all objects managed by this controller.
        """

        # TODO: Allow re-fetching objects
        # - fire OBJECT_ADDED events for new objects
        # - fire OBJECT_REMOVED events for removed objects

        async for obj in get_objects_by_type(self.config_client, self.vantage_types):
            self._items[obj.id] = cast(T, obj)
            self.emit(VantageEvent.OBJECT_ADDED, cast(T, obj))

        self._logger.info(f"{self.__class__.__name__} fetched objects")

    def subscribe(
        self,
        callback: EventCallback[T],
        id_filter: Union[int, Tuple[int], None] = None,
        event_filter: Union[VantageEvent, Tuple[VantageEvent], None] = None,
    ) -> Callable[[], None]:
        """
        Subscribe to status changes for objects managed by this controller.

        Args:
            callback: The callback to call when an object changes.
            id_filter: The object IDs to subscribe to, all objects if None.
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
            for id in id_filter:
                if id not in self._id_subscriptions:
                    self._id_subscriptions[id] = []
                self._id_subscriptions[id].append(subscription)

        # Return a function to unsubscribe
        def unsubscribe() -> None:
            if id_filter is None:
                self._subscriptions.remove(subscription)
            else:
                for id in id_filter:  # type: ignore[union-attr]
                    if id not in self._id_subscriptions:
                        continue
                    self._id_subscriptions[id].remove(subscription)

        return unsubscribe

    def emit(
        self,
        event_type: VantageEvent,
        obj: T,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Emit an event to subscribers of this controller.

        Args:
            event_type: The type of event to emit.
            obj: The object that the event relates to.
            user_data: User data to pass to the callback.
        """

        if user_data is None:
            user_data = {}

        # Grab a list of subscribers that care about this object
        subscribers = self._subscriptions + self._id_subscriptions.get(obj.id, [])
        for callback, event_filter in subscribers:
            if event_filter is not None and event_type not in event_filter:
                continue

            if iscoroutinefunction(callback):
                asyncio.create_task(callback(event_type, obj, user_data))
            else:
                callback(event_type, obj, user_data)


class StatefulController(BaseController[T]):
    # Which Vantage status types this controller handles, if any
    status_types: Optional[Tuple[str, ...]] = None

    # Should we subscribe to status updates from the event log?
    event_log_status: bool = False

    # Which status methods this controller handles from the event log
    event_log_status_methods: Optional[Tuple[str, ...]] = None

    @abstractmethod
    async def fetch_object_state(self, id: int) -> None:
        ...

    @abstractmethod
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        ...

    async def initialize(self) -> None:
        """
        Initialize a stateful controller by populating the objects it manages, fetching
        their initial state, and subscribing to state updates.
        """

        # TODO: Allow reinitalization
        # TODO: Allow initializing without subscribing to object state updates

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
        """
        Fetch the full state of all objects managed by this controller.
        """

        await asyncio.gather(
            *[self.fetch_object_state(obj.id) for obj in self._items.values()]
        )

        self._logger.info(f"{self.__class__.__name__} fetched full state")

    async def subscribe_to_updates(self) -> None:
        """
        Subscribe to state updates for objects managed by this controller.
        """

        # TODO: Handle unsubscribe

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

        self._logger.info(f"{self.__class__.__name__} subscribed to updates")

    def update_state(self, id: int, state: Dict[str, Any]) -> None:
        """
        Update the state of an object and notify subscribers if it changed

        Args:
            id: The ID of the object to update.
            state: A dictionary of attributes to update.
        """

        # Get the object, skip if it doesn't exist
        obj = self.get(id)
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
                self._logger.warn(f"Object '{obj.id}' has no attribute '{key}'")

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

            if event["id"] not in self._items.keys():
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

            id = int(id_str)
            if id not in self._items.keys():
                return

            # Pass the event to the controller
            self.handle_object_update(id, method, args)

        elif event["tag"] == EventType.RECONNECTED:
            # Handle reconnect events

            # Fetch the full state
            await self.fetch_full_state()
