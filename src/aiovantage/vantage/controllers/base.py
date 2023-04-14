import asyncio
import logging
from inspect import iscoroutinefunction
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from aiovantage.aci_client.helpers import get_objects_by_type
from aiovantage.aci_client.system_objects import SystemObject
from aiovantage.hc_client import StatusType
from aiovantage.vantage.query import QuerySet

T = TypeVar("T", bound="SystemObject")

if TYPE_CHECKING:
    from aiovantage.vantage import Vantage


EventCallBackType = Callable[[T, Sequence[str]], None]


class BaseController(Generic[T], QuerySet[T]):
    """Holds and manages all items for a specific Vantage object type."""

    item_cls: Type[T]
    vantage_types: Sequence[str]
    status_types: Optional[Sequence[StatusType]] = None

    def __init__(self, vantage: "Vantage") -> None:
        """
        Create a new controller instance.

        Args:
            vantage: The Vantage client instance
        """

        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._subscribers: List[EventCallBackType[T]] = []
        self._id_subscribers: Dict[int, List[EventCallBackType[T]]] = {}
        self._logger = logging.getLogger(__package__)

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

        # Populate the objects
        async for obj in get_objects_by_type(
            self._vantage._aci_client, list(self.vantage_types), self.item_cls
        ):
            self._items[obj.id] = obj

        # Fetch initial state of known objects
        await self._fetch_initial_states()

        # Subscribe to status events
        if self.status_types is not None:
            await self._vantage._hc_client.subscribe(
                self._handle_status_event, self.status_types
            )

        self._logger.info(f"{self.__class__.__name__} initialized")

    def subscribe(
        self,
        callback: EventCallBackType[T],
        id_filter: Union[int, Sequence[int], None] = None,
    ) -> Callable[[], None]:
        """
        Subscribe to status changes for objects managed by this controller.

        Args:
            callback: The callback to call when an object changes.
            id_filter: The object IDs to subscribe to. Subscribe to all objects if None.
        """

        if isinstance(id_filter, int):
            id_filter = (id_filter,)

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
                for id in id_filter:  # type: ignore[union-attr]
                    if id not in self._id_subscribers:
                        continue
                    self._id_subscribers[id].remove(callback)

        return unsubscribe

    def _handle_status_event(
        self, type: StatusType, vid: int, args: Sequence[str]
    ) -> None:
        """Handle a status event from the Host Command client"""

        # Ignore events for objects we don't know about
        obj = self._items.get(vid)
        if obj is None:
            self._logger.warning(f"Received status event for unknown object {vid}")
            return

        # Delegate to subclasses to update the existing object
        self._update_object_state(vid, args)

        # Notify subscribers
        subscribers = self._subscribers + self._id_subscribers.get(vid, [])
        for callback in subscribers:
            if iscoroutinefunction(callback):
                asyncio.create_task(callback(obj, args))
            else:
                callback(obj, args)

    def _update_object_state(self, vid: int, args: Sequence[str]) -> None:
        # Subclasses should override this method to update object state based on args
        self._logger.warning(
            f"Received event for controller with no event handler {type(self).__name__}"
        )

    async def _fetch_initial_states(self) -> None:
        # Subclasses should override this method to fetch initial state of all objects
        pass
