import logging
from collections.abc import Callable, Iterator, Sequence
from typing import TYPE_CHECKING, Any, Generic, Type, TypeVar, overload

from ..clients.hc import StatusType
from ..models.vantage_object import VantageObject
from ..query import QuerySet

T = TypeVar("T", bound="VantageObject")

if TYPE_CHECKING:
    from aiovantage import Vantage


EventCallBackType = Callable[[T, Sequence[str]], None]


class BaseController(Generic[T]):
    """Holds and manages all items for a specific Vantage object type."""

    item_cls: Type[T]
    vantage_types: tuple[str, ...]
    status_types: tuple[StatusType, ...] | None = None

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize the controller."""
        self._vantage = vantage
        self._items: dict[int, T] = {}
        self._queryset: QuerySet[T] = QuerySet(self._items.values())
        self._subscribers: list[EventCallBackType] = []
        self._id_subscribers: dict[int, list[EventCallBackType]] = {}
        self._logger = logging.getLogger(__package__)
        self._initialized = False

    def __iter__(self) -> Iterator[T]:
        """Iterate items."""
        return iter(self._queryset)

    def __getitem__(self, id: int) -> T:
        """Get item by id."""
        return self._items[id]

    def __contains__(self, id: str) -> bool:
        """Return bool if id is in items."""
        return id in self._items

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
            await self._vantage._hc_client.subscribe(
                self._handle_status_event, self.status_types
            )
            self._logger.info(f"{self.__class__.__name__} subscribed to object updates")

        self._initialized = True

    def subscribe(
        self,
        callback: EventCallBackType,
        id_filter: int | tuple[int, ...] | None = None,
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

    def _handle_status_event(
        self, type: StatusType, vid: int, args: Sequence[str]
    ) -> None:
        """Handle object update event."""
        if vid not in self._items:
            return

        # Update object state
        self._items[vid].status_handler(type, args)

        # Notify subscribers
        subscribers = self._subscribers + self._id_subscribers.get(vid, [])
        for callback in subscribers:
            callback(self._items[vid], args)

    @overload
    def filter(self, match: Callable[[T], Any]) -> "QuerySet[T]":
        ...

    @overload
    def filter(self, **kwargs: Any) -> "QuerySet[T]":
        ...

    def filter(self, *args: Callable[[T], Any], **kwargs: Any) -> QuerySet[T]:
        return self._queryset.filter(*args, **kwargs)

    @overload
    def get(self, id: int, default: T | None = None) -> T | None:
        ...

    @overload
    def get(self, match: Callable[[T], Any]) -> T | None:
        ...

    @overload
    def get(self, **kwargs: Any) -> T | None:
        ...

    def get(self, *args: Callable[[T], Any] | None, **kwargs: Any) -> T | None:
        if len(args) == 1 and isinstance(args[0], int):
            return self._items.get(args[0], kwargs.get("default", None))

        return self._queryset.get(*args, **kwargs)
