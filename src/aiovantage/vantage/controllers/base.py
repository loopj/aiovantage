import asyncio
import logging
from abc import ABC, abstractmethod
from enum import Enum
from inspect import iscoroutinefunction
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.helpers import get_objects_by_type
from aiovantage.aci_client.system_objects import SystemObject, xml_tag_from_class
from aiovantage.hc_client import HCClient
from aiovantage.vantage.query import QuerySet

T = TypeVar("T", bound="SystemObject")


class EventType(Enum):
    OBJECT_ADDED = "add"
    OBJECT_UPDATED = "update"
    OBJECT_DELETED = "delete"


class EventCallback(Protocol):
    def __call__(self, event_type: EventType, obj: T, **kwargs: Any) -> None:
        ...


EventSubscription = Tuple[EventCallback, Optional[Iterable[EventType]]]


class BaseController(Generic[T], QuerySet[T], ABC):
    # The base class of the items that this controller handles
    item_cls: Type[T]

    # The Vantage object types that this controller handles
    vantage_types: Tuple[Type[Any], ...]

    def __init__(self, aci_client: ACIClient) -> None:
        self._aci_client = aci_client
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
        self._subscriptions: List[EventSubscription] = []
        self._id_subscriptions: Dict[int, List[EventSubscription]] = {}
        self._populated = False

        QuerySet.__init__(self, self._items)

    def __getitem__(self, id: int) -> T:
        return self._items[id]

    def __contains__(self, id: int) -> bool:
        return id in self._items

    async def initialize(self) -> None:
        # TODO: Allow re-initialization, and track which objects ids were added/removed

        if self._populated:
            return

        # Populate the objects
        vantage_types = [xml_tag_from_class(cls) for cls in self.vantage_types]
        async for obj in get_objects_by_type(
            self._aci_client, vantage_types, self.item_cls
        ):
            self._items[obj.id] = obj
            self.emit(EventType.OBJECT_ADDED, obj)

        self._populated = True
        self._logger.info(f"{self.__class__.__name__} initialized")

    def subscribe(
        self,
        callback: EventCallback,
        id_filter: Union[int, Tuple[int], None] = None,
        event_filter: Union[EventType, Tuple[EventType], None] = None,
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
        if isinstance(event_filter, EventType):
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

    def emit(self, event_type: EventType, obj: T, **kwargs: Any) -> None:
        subscribers = self._subscriptions + self._id_subscriptions.get(obj.id, [])
        for callback, event_filter in subscribers:
            if event_filter is not None and event_type not in event_filter:
                continue

            if iscoroutinefunction(callback):
                asyncio.create_task(callback(event_type, obj, **kwargs))
            else:
                callback(event_type, obj, **kwargs)


class StatefulController(BaseController[T]):
    # The Vantage status types that this controller handles
    status_types: Optional[Sequence[str]] = None

    # Whether to subscribe to object status events
    object_status: bool = False

    def __init__(self, aci_client: ACIClient, hc_client: HCClient) -> None:
        super().__init__(aci_client)

        self._hc_client = hc_client

    @abstractmethod
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @abstractmethod
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...

    async def initialize(self) -> None:
        await super().initialize()

        # Fetch initial state for all objects
        for obj in self._items.values():
            await self.fetch_initial_state(obj.id)

        # Subscribe to "category" state updates (STATUS {category} -> S:{category})
        if self.status_types:
            await self._hc_client.subscribe(
                self._handle_status_event, status_types=self.status_types
            )

        # Subscribe to "object" state updates (ADDSTATUS {id} -> S:STATUS {id})
        if self.object_status:
            await self._hc_client.subscribe(
                self._handle_status_event, object_ids=self._items.keys()
            )

    def _handle_status_event(
        self, status_type: str, vid: int, args: Sequence[str]
    ) -> None:
        # Ignore events for objects we don't own
        if vid not in self._items:
            return

        # Delegate to subclasses to update the existing object
        self.handle_state_change(vid, status_type, args)

    def _update_and_notify(self, id: int, **kwargs: Any) -> None:
        # Update the state of an object and notify subscribers if it changed

        obj = self.get(id)
        if obj is None:
            return

        # Check if any of the attributes changed and update them
        attrs_changed = []
        for key, value in kwargs.items():
            try:
                if getattr(obj, key) != value:
                    setattr(obj, key, value)
                    attrs_changed.append(key)
            except AttributeError:
                self._logger.warn(f"Object '{obj.id}' has no attribute '{key}'")

        # Notify subscribers
        if len(attrs_changed) > 0:
            self.emit(EventType.OBJECT_UPDATED, obj, attrs_changed=attrs_changed)
