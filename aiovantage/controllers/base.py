import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from ..clients.hc import StatusType
from ..models.vantage_object import VantageObject
from ..query import QuerySet

T = TypeVar("T", bound="VantageObject")

if TYPE_CHECKING:
    from aiovantage import Vantage


EventCallBackType = Callable[[T, List[str]], None]

class BaseController(Generic[T]):
    """Holds and manages all items for a specific Vantage object type."""

    item_cls: Type[T]
    vantage_types: Iterable[str]
    status_types: Union[Tuple[StatusType, ...], None] = None

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize the controller."""
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._queryset: QuerySet[T] = QuerySet(self._items.values())
        self._subscribers: List[EventCallBackType] = []
        self._id_subscribers: Dict[int, List[EventCallBackType]] = {}
        self._logger = logging.getLogger(__package__)
        self._initialized = False

    async def fetch_objects(self, keep_updated: bool = True) -> None:
        # Fetch initial object details
        objects = await self._vantage._aci_client.fetch_objects(self.vantage_types)
        for el in objects:
            item = self.item_cls.from_xml_el(el)
            item._vantage = self._vantage
            self._items[item.id] = item

        self._logger.info(f"{self.__class__.__name__} loaded objects")

        # Subscribe to status updates
        # TODO: should we await here or should this run in the background?
        if keep_updated and self.status_types is not None:
            await self._vantage._hc_client.subscribe(self._handle_status_event, self.status_types)
            self._logger.info(f"{self.__class__.__name__} subscribed to object updates")

        self._initialized = True

    def subscribe(
            self,
            callback: EventCallBackType,
            id_filter: Union[int, Tuple[int], None] = None,
    ) -> None:
        if id_filter is None:
            self._subscribers.append(callback)
        else:
            if not isinstance(id_filter, (list, tuple)):
                id_filter = (id_filter,)

            for id in id_filter:
                if id not in self._id_subscribers:
                    self._id_subscribers[id] = []
                self._id_subscribers[id].append(callback)

    def _handle_status_event(self, type: StatusType, vid: int, args: list[str]) -> None:
        """Handle object update event."""
        if vid not in self._items:
            return

        # Update object state
        self._items[vid].status_handler(args)

        # Notify subscribers
        subscribers = self._subscribers + self._id_subscribers.get(vid, [])
        for callback in subscribers:
            callback(self._items[vid], args)

    def get(self, *args: Optional[Callable[[T], bool]], **kwargs: Any) -> Optional[T]:
        if not self._initialized:
            self._logger.debug(f"{type(self).__name__} not yet initialized")

        return self._queryset.get(*args, **kwargs)

    def filter(
        self, *args: Optional[Callable[[T], bool]], **kwargs: Any
    ) -> QuerySet[T]:
        if not self._initialized:
            self._logger.debug(f"{type(self).__name__} not yet initialized")

        return self._queryset.filter(*args, **kwargs)

    def __iter__(self) -> Iterator[T]:
        """Iterate items."""
        if not self._initialized:
            self._logger.debug(f"{type(self).__name__} not yet initialized")

        return iter(self._queryset)

    def __getitem__(self, id: int) -> T:
        """Get item by id."""
        if not self._initialized:
            self._logger.debug(f"{type(self).__name__} not yet initialized")

        return self._items[id]

    def __contains__(self, id: str) -> bool:
        """Return bool if id is in items."""
        if not self._initialized:
            self._logger.debug(f"{type(self).__name__} not yet initialized")

        return id in self._items
