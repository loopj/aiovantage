from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Iterator
from typing import Any, TypeVar, overload

from typing_extensions import Self

T = TypeVar("T")


class QuerySet(Iterable[T], AsyncIterator[T]):
    """Queryset class for querying objects from a dictionary.

    Querysets are iterable and async iterable, and can be chained together to
    filter objects.
    """

    def __init__(
        self,
        data: dict[int, T],
        populate: Callable[[], Awaitable[None]],
        filters: list[Callable[[T], Any]] | None = None,
    ) -> None:
        """Initialize a queryset.

        Args:
            data: The data dictionary to query.
            populate: A coroutine to populate the data so we don't have a complete
                      dataset before using "async for" loops.
            filters: A list of filters to apply to the queryset.
        """
        self._data = data
        self._populate = populate
        self._iterator: Iterator[T] | None = None

        if filters is None:
            self.__filters: list[Callable[[T], Any]] = []
        else:
            self.__filters = filters

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the queryset."""
        for obj in self._data.values():
            if all(filter_fn(obj) for filter_fn in self.__filters):
                yield obj

    def __bool__(self) -> bool:
        """Return True if the queryset contains any objects."""
        return any(True for _ in self)

    def __aiter__(self) -> Self:
        """Return an async iterator over the queryset."""
        self.__iterator = None
        return self

    async def __anext__(self) -> T:
        """Return the next object in the queryset."""
        if self.__iterator is None:
            await self._populate()

            self.__iterator = iter(self)

        try:
            return next(self.__iterator)
        except StopIteration as exc:
            raise StopAsyncIteration from exc

    @overload
    def filter(self, match: Callable[[T], Any]) -> "QuerySet[T]": ...

    @overload
    def filter(self, **kwargs: Any) -> "QuerySet[T]": ...

    def filter(self, *args: Any, **kwargs: Any) -> "QuerySet[T]":
        """Return a queryset of objects that match the given filter."""
        queryset = QuerySet(self._data, self._populate, self.__filters.copy())

        if len(args) == 1:
            queryset.__filters.append(args[0])
        elif len(args) == 0 and len(kwargs) > 0:
            queryset.__filters.append(
                lambda obj: all(
                    getattr(obj, key) == value for key, value in kwargs.items()
                )
            )
        else:
            raise TypeError("filter() and get() expect either a callable or **kwargs")

        return queryset

    @overload
    def get(self, key: int) -> T | None: ...

    @overload
    def get(self, match: Callable[[T], Any]) -> T | None: ...

    @overload
    def get(self, **kwargs: Any) -> T | None: ...

    def get(self, *args: Any, **kwargs: Any) -> T | None:
        """Get the first object that matches the given filter."""
        # Handle the case where we're getting an object by key
        if len(args) == 1 and isinstance(args[0], int):
            return self._data.get(args[0], None)

        # Otherwise, pass through to filter and return the first object
        return next(iter(self.filter(*args, **kwargs)), None)

    @overload
    async def aget(self, key: int) -> T | None: ...

    @overload
    async def aget(self, match: Callable[[T], Any]) -> T | None: ...

    @overload
    async def aget(self, **kwargs: Any) -> T | None: ...

    async def aget(self, *args: Any, **kwargs: Any) -> T | None:
        """Asynchronously get the first object that matches the given filter."""
        await self._populate()
        return self.get(*args, **kwargs)

    def first(self) -> T | None:
        """Return the first object in the queryset."""
        return next(iter(self), None)

    async def afirst(self) -> T | None:
        """Asynchronously return the first object in the queryset."""
        await self._populate()
        return self.first()
