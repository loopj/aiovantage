import logging
from collections.abc import AsyncIterator, Callable, Iterator, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Optional,
    TypeVar,
    Union,
    overload,
)

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler

from aiovantage.aci_client.interfaces.configuration import (
    open_filter,
    get_filter_results,
    close_filter,
)
from aiovantage.hc_client import StatusType
from aiovantage.models.system_object import SystemObject
from aiovantage.query import QuerySet

T = TypeVar("T", bound="SystemObject")

if TYPE_CHECKING:
    from aiovantage import Vantage


EventCallBackType = Callable[[T, Sequence[str]], None]


class BaseController(Generic[T]):
    """Holds and manages all items for a specific Vantage object type."""

    # TODO: ClassVar for these?
    item_cls: type[T]
    vantage_types: tuple[str, ...]
    status_types: Optional[tuple[StatusType, ...]] = None

    def __init__(self, vantage: "Vantage") -> None:
        """Initialize the controller."""
        self._vantage = vantage
        self._items: dict[int, T] = {}
        self._queryset: QuerySet[T] = QuerySet(self._items.values())
        self._subscribers: list[EventCallBackType] = []
        self._id_subscribers: dict[int, list[EventCallBackType]] = {}
        self._logger = logging.getLogger(__package__)
        self._initialized = False
        self._parser = XmlParser(
            handler=XmlEventHandler,
            config=ParserConfig(
                fail_on_unknown_properties=False,
                fail_on_unknown_attributes=False,
            ),
        )

    def __iter__(self) -> Iterator[T]:
        """Iterate items."""
        return iter(self._queryset)

    def __getitem__(self, id: int) -> T:
        """Get item by id."""
        return self._items[id]

    def __contains__(self, id: str) -> bool:
        """Return bool if id is in items."""
        return id in self._items

    async def _fetch_objects(self) -> AsyncIterator:
        # Build the "xpath" filter
        xpath = None
        if self.vantage_types is not None:
            xpath = " or ".join([f"/{str}" for str in self.vantage_types])

        # Open the filter
        handle = (await open_filter(self._vantage._aci_client, xpath)).handle

        # Get the results
        while True:
            response = await get_filter_results(self._vantage._aci_client, handle)
            if not response:
                break

            for object in response:
                yield self._parser.parse(object[0], self.item_cls)

        # Close the filter
        await close_filter(self._vantage._aci_client, handle)

    async def subscribe_to_object_updates(self) -> None:
        if self.status_types is not None:
            await self._vantage._hc_client.subscribe(
                self._handle_status_event, self.status_types
            )
            self._logger.info(f"{self.__class__.__name__} subscribed to object updates")

    async def initialize(self) -> None:
        async for obj in self._fetch_objects():
            obj._vantage = self._vantage
            self._items[obj.id] = obj

        if self.status_types is not None:
            await self._vantage._hc_client.subscribe(
                self._handle_status_event, self.status_types
            )

        self._logger.info(f"{self.__class__.__name__} initialized")
        self._initialized = True

    def subscribe(
        self,
        callback: EventCallBackType,
        id_filter: Union[int, tuple[int, ...], None] = None,
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

    def all(self) -> QuerySet[T]:
        """Return a queryset of all items."""
        return self._queryset

    @overload
    def filter(self, match: Callable[[T], Any]) -> "QuerySet[T]":
        ...

    @overload
    def filter(self, **kwargs: Any) -> "QuerySet[T]":
        ...

    def filter(self, *args: Callable[[T], Any], **kwargs: Any) -> QuerySet[T]:
        return self._queryset.filter(*args, **kwargs)

    @overload
    def get(self, id: int, default: Optional[T] = None) -> Optional[T]:
        ...

    @overload
    def get(self, match: Callable[[T], Any]) -> Optional[T]:
        ...

    @overload
    def get(self, **kwargs: Any) -> Optional[T]:
        ...

    def get(self, *args: Optional[Callable[[T], Any]], **kwargs: Any) -> Optional[T]:
        if len(args) == 1 and isinstance(args[0], int):
            return self._items.get(args[0], kwargs.get("default", None))

        return self._queryset.get(*args, **kwargs)
