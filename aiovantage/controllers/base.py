import logging
import xml.etree.ElementTree as ET
from typing import (TYPE_CHECKING, Any, Callable, Dict, Generic, Iterable,
                    Iterator, List, Optional, Type, TypeVar)

from ..models.base import Base
from ..query import QuerySet

T = TypeVar("T", bound="Base")

if TYPE_CHECKING:
    from aiovantage import Vantage


class BaseController(Generic[T]):
    """Holds and manages all items for a specific Vantage object type."""

    item_cls: Type[T]
    vantage_types: Iterable[str]
    event_types: Optional[Iterable[str]] = None

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize the controller."""
        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._queryset: QuerySet[T] = QuerySet(self._items.values())
        self._subscribers: List[Callable[[T, list], None]] = []
        self._logger = logging.getLogger(__package__)
        self._initialized = False

    async def initialize(self) -> None:
        """
        Initialize controller by fetching all items for this object  type.

        Must be called only once. Any updates will be retrieved by events.
        """

        # Fetch initial object details
        objects = await self._vantage._aci_client.fetch_objects(self.vantage_types)
        for el in objects:
            obj = self.from_xml(el)
            obj._vantage = self._vantage
            self._items[obj.id] = obj

        # Subscribe to object updates
        if self.event_types is not None:
            await self._vantage._events_client.subscribe(
                self._handle_event, *self.event_types
            )

        self._logger.info(f"Initialized {self.__class__.__name__}")

    def subscribe(self, callback: Callable[[T, list], None]) -> None:
        self._subscribers.append(callback)

    def from_xml(self, el: ET.Element) -> T:
        raise NotImplementedError()

    def handle_event(self, obj: T, args: Any) -> None:
        raise NotImplementedError()

    def get(self, *args: Optional[Callable[[T], bool]], **kwargs: Any) -> Optional[T]:
        return self._queryset.get(*args, **kwargs)

    def filter(
        self, *args: Optional[Callable[[T], bool]], **kwargs: Any
    ) -> QuerySet[T]:
        return self._queryset.filter(*args, **kwargs)

    def __getitem__(self, id: int) -> T:
        """Get item by id."""
        return self._items[id]

    def __iter__(self) -> Iterator[T]:
        """Iterate items."""
        return iter(self._items.values())

    def __contains__(self, id: str) -> bool:
        """Return bool if id is in items."""
        return id in self._items

    def _handle_event(self, type: str, vid: int, args: list) -> None:
        if vid in self._items:
            self.handle_event(self._items[vid], args)

        for callback in self._subscribers:
            callback(self[vid], args)