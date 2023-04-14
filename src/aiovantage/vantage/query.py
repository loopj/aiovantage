from collections.abc import Callable, Iterator
from typing import Any, Dict, Generic, List, Optional, TypeVar, overload

T = TypeVar("T")


class QuerySet(Generic[T]):
    def __init__(self, data: Dict[int, T]) -> None:
        self._data: Dict[int, T] = data
        self._filters: List[Callable[[T], Any]] = []

    def __iter__(self) -> Iterator[T]:
        for obj in self._data.values():
            if all(filter(obj) for filter in self._filters):
                yield obj

    @overload
    def filter(self, match: Callable[[T], Any]) -> "QuerySet[T]":
        """
        Return a queryset of objects that match the given predicate.

        Args:
            match: The predicate to match.

        Returns:
            A queryset of matching objects
        """
        ...

    @overload
    def filter(self, **kwargs: Any) -> "QuerySet[T]":
        """
        Return a queryset of items that match the given keyword arguments.

        Args:
            kwargs: The keyword arguments to match.

        Returns:
            A queryset of matching objects
        """
        ...

    def filter(self, *args: Callable[[T], Any], **kwargs: Any) -> "QuerySet[T]":
        qs = QuerySet(self._data)
        qs._filters = self._filters.copy()

        if len(args) == 1:
            qs._filters.append(args[0])
        elif len(args) == 0 and len(kwargs) > 0:
            qs._filters.append(
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
        Get the first object that matches the given kwargs.

        Args:
            **kwargs: The keyword arguments to match.

        Returns:
            The matching object or None if no object matches
        """
        ...

    def get(self, *args: Callable[[T], Any], **kwargs: Any) -> Optional[T]:
        if len(args) == 1 and isinstance(args[0], int):
            return self._data.get(args[0], kwargs.get("default", None))

        return next(iter(self.filter(*args, **kwargs)), None)
