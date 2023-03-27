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
    Type,
    TypeVar,
)

from ..models.base import Base
from ..query import QuerySet

T = TypeVar("T", bound="Base")

if TYPE_CHECKING:
    from aiovantage import Vantage


class BaseController(Generic[T]):
    item_type: Type[T]
    vantage_types: Iterable[str]
    event_types: Optional[Iterable[str]] = None

    _datastore: Dict[int, T]
    _queryset: QuerySet[T]
    _subscribers: List[Callable[[T, list], None]]
    _logger: logging.Logger

    def __init__(self) -> None:
        self._datastore = {}
        self._queryset = QuerySet(self._datastore.values())
        self._subscribers = []
        self._logger = logging.getLogger(__name__)

    def __getitem__(self, id: int) -> T:
        """Get item by id."""
        return self._datastore[id]

    def __contains__(self, id: str) -> bool:
        """Return bool if id is in items."""
        return id in self._datastore

    def __iter__(self) -> Iterator[T]:
        """Iterate items."""
        return iter(self._datastore.values())

    async def initialize(self, vantage: "Vantage") -> None:
        # Fetch initial object details
        objects = await vantage._aci_client.fetch_objects(self.vantage_types)
        for el in objects:
            obj = self.item_type.from_xml(el)
            obj._vantage = vantage
            self._datastore[obj.id] = obj

        # Subscribe to object updates
        if self.event_types is not None:
            await vantage._events_client.subscribe(
                self._handle_event, *self.event_types
            )

        self._logger.info(f"Initialized {self.__class__.__name__}")

    def _handle_event(self, type: str, vid: int, args: list) -> None:
        if vid in self._datastore:
            self.handle_event(self._datastore[vid], args)

        for callback in self._subscribers:
            callback(self[vid], args)

    def handle_event(self, obj: T, args: Any) -> None:
        pass

    def subscribe(self, callback: Callable[[T, list], None]) -> None:
        self._subscribers.append(callback)

    def get(self, *args: Optional[Callable[[T], bool]], **kwargs: Any) -> Optional[T]:
        return self._queryset.get(*args, **kwargs)

    def filter(
        self, *args: Optional[Callable[[T], bool]], **kwargs: Any
    ) -> QuerySet[T]:
        return self._queryset.filter(*args, **kwargs)
