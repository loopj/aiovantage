from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    TypeVar,
    overload,
)

T = TypeVar("T")


class QuerySet(Iterable[T], AsyncIterator[T]):
    """
    A basic django-ish queryset class for querying objects from an integer-keyed
    dictionary of objects. Querysets are iterable and async iterable, and can be
    chained together to filter objects.
    """

    def __init__(
        self, data: Dict[int, T], populate: Callable[[], Awaitable[None]]
    ) -> None:
        """
        Args:
            data: The data dictionary to query.
            populate: A coroutine to populate the data so we don't have a complete
                      dataset before using "async for" loops.
        """

        self.__data: Dict[int, T] = data
        self.__populate: Callable[[], Awaitable[None]] = populate
        self.__filters: List[Callable[[T], Any]] = []
        self.__iterator: Optional[Iterator[T]] = None

    def __iter__(self) -> Iterator[T]:
        for obj in self.__data.values():
            if all(filter(obj) for filter in self.__filters):
                yield obj

    def __aiter__(self) -> AsyncIterator[T]:
        self.__iterator = None
        return self

    async def __anext__(self) -> T:
        if self.__iterator is None:
            if self.__populate is not None:
                await self.__populate()

            self.__iterator = iter(self)

        try:
            return next(self.__iterator)
        except StopIteration:
            raise StopAsyncIteration

    @overload
    def filter(self, match: Callable[[T], Any]) -> "QuerySet[T]":
        """
        Return a queryset of objects that match the given predicate.

        Args:
            match: The predicate to filter by.

        Returns:
            A queryset of matching objects.
        """
        ...

    @overload
    def filter(self, **kwargs: Any) -> "QuerySet[T]":
        """
        Return a queryset of items that match the properties in the given keyword args.

        Args:
            kwargs: The keyword arguments to filter by.

        Returns:
            A queryset of matching objects.
        """
        ...

    def filter(self, *args: Callable[[T], Any], **kwargs: Any) -> "QuerySet[T]":
        qs = QuerySet(self.__data, self.__populate)
        qs.__filters = self.__filters.copy()

        if len(args) == 1:
            qs.__filters.append(args[0])
        elif len(args) == 0 and len(kwargs) > 0:
            qs.__filters.append(
                lambda obj: all(
                    getattr(obj, key) == value for key, value in kwargs.items()
                )
            )
        else:
            raise TypeError("filter() and get() expect either a callable or **kwargs")

        return qs

    @overload
    def get(self, id: int, default: Optional[T] = None) -> Optional[T]:
        """
        Get the object with the given id.

        Args:
            id: The id of the object to get.
            default: The default value to return if the object is not found.

        Returns:
            The matching object, or the default value if the object is not found.
        """
        ...

    @overload
    def get(self, match: Callable[[T], Any]) -> Optional[T]:
        """
        Get the first object that matches the given predicate.

        Args:
            match: The predicate to match.

        Returns:
            The matching object or None if no object matches
        """
        ...

    @overload
    def get(self, **kwargs: Any) -> Optional[T]:
        """
        Get the first object that matches the properties in the given keyword args.

        Args:
            **kwargs: The keyword arguments to match.

        Returns:
            The matching object or None if no object matches
        """
        ...

    def get(self, *args: Callable[[T], Any], **kwargs: Any) -> Optional[T]:
        # Handle the case where we're getting an object by id
        if len(args) == 1 and isinstance(args[0], int):
            return self.__data.get(args[0], kwargs.get("default", None))

        # Otherwise, pass through to filter and return the first object
        return next(iter(self.filter(*args, **kwargs)), None)

    @overload
    async def aget(self, id: int, default: Optional[T] = None) -> Optional[T]:
        """
        Asynchronously get the object with the given id.

        Args:
            id: The id of the object to get.
            default: The default value to return if the object is not found.

        Returns:
            A coroutine which returns the matching object or None if no object matches
        """
        ...

    @overload
    async def aget(self, match: Callable[[T], Any]) -> Optional[T]:
        """
        Asynchronously get the first object that matches the properties in the given
        keyword args.

        Args:
            match: The predicate to match.

        Returns:
            A coroutine which returns the matching object or None if no object matches
        """
        ...

    @overload
    async def aget(self, **kwargs: Any) -> Optional[T]:
        """
        Asynchronously get the first object that matches the properties in the given
        keyword args.

        Args:
            **kwargs: The keyword arguments to match.

        Returns:
            A coroutine which returns the matching object or None if no object matches
        """
        ...

    async def aget(self, *args: Callable[[T], Any], **kwargs: Any) -> Optional[T]:
        await self.__populate()
        return self.get(*args, **kwargs)
