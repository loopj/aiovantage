import logging
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    overload,
)

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler

from aiovantage.aci_client.interfaces import IConfiguration
from aiovantage.aci_client.methods.configuration import (
    CloseFilter,
    GetFilterResults,
    ObjectFilter,
    OpenFilter,
)
from aiovantage.aci_client.system_objects import SystemObject
from aiovantage.hc_client import StatusType
from aiovantage.query import QuerySet

T = TypeVar("T", bound="SystemObject")

if TYPE_CHECKING:
    from aiovantage import Vantage


EventCallBackType = Callable[[T, Sequence[str]], None]


class BaseController(Generic[T]):
    """Holds and manages all items for a specific Vantage object type."""

    item_cls: Type[T]
    vantage_types: Iterable[str]
    status_types: Optional[Sequence[StatusType]] = None

    def __init__(self, vantage: "Vantage") -> None:
        """
        Initialize the controller.

        Args:
            vantage: The Vantage client instance to use.
        """

        self._vantage = vantage
        self._items: Dict[int, T] = {}
        self._queryset: QuerySet[T] = QuerySet(self._items.values())
        self._subscribers: List[EventCallBackType[T]] = []
        self._id_subscribers: Dict[int, List[EventCallBackType[T]]] = {}
        self._logger = logging.getLogger(__package__)

        self._parser = XmlParser(
            handler=XmlEventHandler,
            config=ParserConfig(
                fail_on_unknown_properties=False,
                fail_on_unknown_attributes=False,
            ),
        )

    def __iter__(self) -> Iterator[T]:
        return iter(self._queryset)

    def __getitem__(self, id: int) -> T:
        return self._items[id]

    def __contains__(self, id: int) -> bool:
        return id in self._items

    async def _fetch_objects(self) -> AsyncIterator[T]:
        # Open the filter
        handle = await self._vantage._aci_client.request(
            IConfiguration,
            OpenFilter,
            OpenFilter.Params(
                objects=ObjectFilter(object_type=list(self.vantage_types))
            ),
        )

        # Get the results
        while True:
            response = await self._vantage._aci_client.request(
                IConfiguration,
                GetFilterResults,
                GetFilterResults.Params(h_filter=handle),
            )

            if not response.object_value:
                break

            for object in response.object_value:
                if object.choice and isinstance(object.choice, self.item_cls):
                    yield object.choice
                else:
                    self._logger.warning(f"Couldnt parse object with vid {object.id}")

        # Close the filter
        await self._vantage._aci_client.request(IConfiguration, CloseFilter, handle)

    async def initialize(self) -> None:
        """
        Initialize the controller by fetching all objects from the ACI service, and
        subscribing to status updates from the HC service.
        """

        # Populate the objects
        async for obj in self._fetch_objects():
            self._items[obj.id] = obj

        # Subscribe to status events
        if self.status_types is not None:
            await self._vantage._hc_client.subscribe(
                self._handle_status_event, self.status_types
            )

        self._logger.info(f"{self.__class__.__name__} initialized")

    def subscribe(
        self,
        callback: EventCallBackType[T],
        id_filter: Union[int, Iterable[int], None] = None,
    ) -> None:
        """
        Subscribe to status changes for objects managed by this controller.

        Args:
            callback: The callback to call when an object changes.
            id_filter: The object IDs to subscribe to. If None, subscribe to all objects.
        """

        if id_filter is None:
            self._subscribers.append(callback)
        else:
            if isinstance(id_filter, int):
                id_filter = (id_filter,)

            for id in id_filter:
                if id not in self._id_subscribers:
                    self._id_subscribers[id] = []
                self._id_subscribers[id].append(callback)

    def _handle_status_event(
        self, type: StatusType, vid: int, args: Sequence[str]
    ) -> None:
        """Handle a status event from the Host Command client"""

        # Ignore events for objects we don't know about
        if vid not in self._items:
            return

        # Update object state
        self.status_handler(type, vid, args)

        # Notify subscribers
        subscribers = self._subscribers + self._id_subscribers.get(vid, [])
        for callback in subscribers:
            callback(self._items[vid], args)

    def status_handler(self, type: StatusType, id: int, args: Sequence[str]) -> None:
        pass

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
