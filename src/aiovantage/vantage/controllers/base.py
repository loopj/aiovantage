import asyncio
import logging
from abc import ABC, abstractmethod
from inspect import iscoroutinefunction
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    TYPE_CHECKING,
)

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects_by_type
from aiovantage.config_client.system_objects import SystemObject
from aiovantage.config_client.xml_dataclass import xml_tag_from_class
from aiovantage.command_client import CommandClient, Event, EventType
from aiovantage.command_client.helpers import tokenize_response
from aiovantage.vantage.events import VantageEvent
from aiovantage.vantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage.vantage import Vantage

T = TypeVar("T", bound="SystemObject")


# Types for callbacks for event subscriptions
EventCallback = Callable[[VantageEvent, T, Dict[str, Any]], None]
EventSubscription = Tuple[EventCallback[T], Optional[Iterable[VantageEvent]]]


class BaseController(Generic[T], QuerySet[T], ABC):
    # The base class of the items that this controller handles
    item_cls: Type[T]

    # The Vantage object types that this controller handles
    vantage_types: Tuple[Type[Any], ...]

    def __init__(self, vantage: "Vantage") -> None:
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscriptions: List[EventSubscription[T]] = []
        self._id_subscriptions: Dict[int, List[EventSubscription[T]]] = {}
        self._populated = False

        QuerySet.__init__(self, self._items)

    def __getitem__(self, id: int) -> T:
        return self._items[id]

    def __contains__(self, id: int) -> bool:
        return id in self._items

    @property
    def command_client(self) -> CommandClient:
        return self._vantage._command_client

    @property
    def config_client(self) -> ConfigClient:
        return self._vantage._config_client

    async def initialize(self) -> None:
        """
        Initialize a stateless controller by populating the objects it manages.
        """

        # TODO: Allow re-initialization, and track which objects ids were added/removed
        # since last initialization

        if self._populated:
            return

        # Populate the objects
        vantage_types = [xml_tag_from_class(cls) for cls in self.vantage_types]
        async for obj in get_objects_by_type(
            self.config_client, vantage_types, self.item_cls
        ):
            self._items[obj.id] = obj
            self.emit(VantageEvent.OBJECT_ADDED, obj)

        self._populated = True
        self._logger.info(f"{self.__class__.__name__} populated")

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

        # Guarantee that user_data dict is present
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

    # Whether to subscribe to the event log for status updates
    event_log_status: bool = False

    @abstractmethod
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @abstractmethod
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...

    async def initialize(self) -> None:
        """
        Initialize a stateful controller by populating the objects it manages, fetching
        their initial state, and subscribing to state updates.
        """

        # Populate the objects
        await super().initialize()

        # Fetch initial state for all objects
        for obj in self._items.values():
            await self.fetch_initial_state(obj.id)

        self._logger.info(f"{self.__class__.__name__} fetched initial state")

        # Don't subscribe to state updates if there are no managed objects
        if len(self._items) == 0:
            return

        # Subscribe to object state updates from the event log
        if self.event_log_status:
            await self._vantage._command_client.subscribe_event_log(
                self._handle_command_client_event, ("STATUS", "STATUSEX")
            )

        # Subscribe to "STATUS {type}" updates, if this controller cares about them
        if self.status_types:
            await self._vantage._command_client.subscribe_status(
                self._handle_command_client_event, self.status_types
            )

        self._logger.info(f"{self.__class__.__name__} monitoring for state changes")

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

    def _handle_command_client_event(self, event: Event) -> None:
        # Handle status update events from the command client

        if event["tag"] == EventType.STATUS:
            # Handle "STATUS {type}" events

            if event["id"] not in self._items.keys():
                return

            self.handle_state_change(event["id"], event["status_type"], event["args"])

        elif event["tag"] == EventType.EVENT_LOG:
            # Handle event log events

            id_str, method, *args = tokenize_response(event["log"])
            id = int(id_str)

            if id not in self._items.keys():
                return

            # Pass the event to the controller
            self.handle_state_change(id, method, args)
