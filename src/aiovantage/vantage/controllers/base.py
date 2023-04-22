import asyncio
import logging
from abc import ABC, abstractmethod
from inspect import iscoroutinefunction
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
)

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.helpers import get_objects_by_type
from aiovantage.aci_client.system_objects import SystemObject, xml_tag_from_class
from aiovantage.hc_client import HCClient
from aiovantage.vantage.query import QuerySet

T = TypeVar("T", bound="SystemObject")


EventCallback = Callable[[T, List[str]], None]


class BaseController(Generic[T], QuerySet[T], ABC):
    # The base class of the items that this controller handles
    item_cls: Type[T]

    # The Vantage object types that this controller handles
    vantage_types: Tuple[Type[Any], ...]

    def __init__(self, aci_client: ACIClient) -> None:
        self._aci_client = aci_client
        self._items: Dict[int, T] = {}
        self._logger = logging.getLogger(__package__)
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

        self._populated = True
        self._logger.info(f"{self.__class__.__name__} initialized")


class StatefulController(BaseController[T]):
    # The Vantage status types that this controller handles
    status_types: Optional[Sequence[str]] = None

    # Whether to subscribe to object status events
    object_status: bool = False

    def __init__(self, aci_client: ACIClient, hc_client: HCClient) -> None:
        super().__init__(aci_client)

        self._hc_client = hc_client
        self._subscribers: List[EventCallback[T]] = []
        self._id_subscribers: Dict[int, List[EventCallback[T]]] = {}

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

    def subscribe(
        self, callback: EventCallback[T], id_filter: Optional[Sequence[int]] = None
    ) -> Callable[[], None]:
        """
        Subscribe to status changes for objects managed by this controller.

        Args:
            callback: The callback to call when an object changes.
            id_filter: The object IDs to subscribe to. Subscribe to all objects if None.

        Returns:
            A function to unsubscribe from the callback.
        """

        if id_filter is None:
            self._subscribers.append(callback)
        else:
            for id in id_filter:
                if id not in self._id_subscribers:
                    self._id_subscribers[id] = []
                self._id_subscribers[id].append(callback)

        # Return a function to unsubscribe
        def unsubscribe() -> None:
            if id_filter is None:
                self._subscribers.remove(callback)
            else:
                for id in id_filter:
                    if id not in self._id_subscribers:
                        continue
                    self._id_subscribers[id].remove(callback)

        return unsubscribe

    @abstractmethod
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @abstractmethod
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...

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
            subscribers = self._subscribers + self._id_subscribers.get(obj.id, [])
            for callback in subscribers:
                if iscoroutinefunction(callback):
                    asyncio.create_task(callback(obj, attrs_changed))
                else:
                    callback(obj, attrs_changed)
