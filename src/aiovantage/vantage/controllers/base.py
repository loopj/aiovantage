import asyncio
import logging
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


class BaseController(Generic[T], QuerySet[T]):
    """Holds and manages all items for a specific Vantage object type."""

    item_cls: Type[T]
    vantage_types: Tuple[Type[Any], ...]
    status_types: Optional[Sequence[str]] = None
    object_status: bool = False

    def __init__(self, aci_client: ACIClient, hc_client: HCClient) -> None:
        """
        Create a new controller instance.

        Args:
            vantage: The Vantage client instance
        """

        self._aci_client = aci_client
        self._hc_client = hc_client
        self._items: Dict[int, T] = {}
        self._subscribers: List[EventCallback[T]] = []
        self._id_subscribers: Dict[int, List[EventCallback[T]]] = {}
        self._logger = logging.getLogger(__package__)
        self._initialized = False

        QuerySet.__init__(self, self._items)

    def __getitem__(self, id: int) -> T:
        return self._items[id]

    def __contains__(self, id: int) -> bool:
        return id in self._items

    async def initialize(self) -> None:
        """
        Initialize the controller by fetching all objects from the ACI service, and
        subscribing to status updates from the HC service.
        """

        if self._initialized:
            return

        # Populate the objects
        vantage_types = [xml_tag_from_class(cls) for cls in self.vantage_types]
        async for obj in get_objects_by_type(
            self._aci_client, vantage_types, self.item_cls
        ):
            self._items[obj.id] = obj

        # Fetch initial state for all objects
        for obj in self._items.values():
            await self._fetch_initial_state(obj.id)

        # Subscribe to "category" events (STATUS {category} -> S:{category})
        if self.status_types:
            await self._hc_client.subscribe(
                self._handle_status_event, status_types=self.status_types
            )

        # Subscribe to object events (ADDSTATUS {id} -> S:STATUS {id})
        if self.object_status:
            await self._hc_client.subscribe(
                self._handle_status_event, object_ids=self._items.keys()
            )

        self._initialized = True
        self._logger.info(f"{self.__class__.__name__} initialized")

    def subscribe(
        self,
        callback: EventCallback[T],
        id_filter: Optional[Sequence[int]] = None,
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

        def unsubscribe() -> None:
            if id_filter is None:
                self._subscribers.remove(callback)
            else:
                for id in id_filter:
                    if id not in self._id_subscribers:
                        continue
                    self._id_subscribers[id].remove(callback)

        return unsubscribe

    def _handle_status_event(
        self, status_type: str, vid: int, args: Sequence[str]
    ) -> None:
        """Handle a status event from the Host Command client"""

        # Ignore events for objects we don't own
        if vid not in self._items:
            return

        # Delegate to subclasses to update the existing object
        self._handle_status(vid, status_type, args)

    def _update_and_notify(self, id: int, **kwargs: Any) -> None:
        # Update the state of an object and notify subscribers if it changed

        obj = self.get(id)
        if obj is None:
            return

        # Check if any of the attributes changed
        attrs_changed = []
        for key, value in kwargs.items():
            try:
                if getattr(obj, key) != value:
                    setattr(obj, key, value)
                    attrs_changed.append(key)
            except AttributeError:
                self._logger.warn(f"Object '{obj.id}' has no attribute '{key}'")

        # Update the object and notify subscribers
        if len(attrs_changed) > 0:
            self._notify_subscribers(obj, attrs_changed)

    def _notify_subscribers(self, obj: T, attrs_changed: List[str]) -> None:
        subscribers = self._subscribers + self._id_subscribers.get(obj.id, [])
        for callback in subscribers:
            if iscoroutinefunction(callback):
                asyncio.create_task(callback(obj, attrs_changed))
            else:
                callback(obj, attrs_changed)

    # Subclasses should override these methods
    async def _fetch_initial_state(self, id: int) -> None:
        ...

    def _handle_status(self, id: int, status_type: str, args: Sequence[str]) -> None:
        ...
