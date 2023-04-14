from collections.abc import Callable, Collection, Iterator
from typing import Any, Generic, List, Optional, TypeVar, overload

T = TypeVar("T")


class QuerySet(Generic[T]):
    def __init__(self, data: Collection[T]) -> None:
        self._data:Collection[T] = data
        self._filters: List[Callable[[T], Any]] = []

    def __iter__(self) -> Iterator[T]:
        for obj in self._data:
            if all(filter(obj) for filter in self._filters):
                yield obj

    def __len__(self) -> int:
        return len(self._data)

    @overload
    def filter(self, match: Callable[[T], Any]) -> "QuerySet[T]":
        ...

    @overload
    def filter(self, **kwargs: Any) -> "QuerySet[T]":
        ...

    def filter(self, *args: Callable[[T], Any], **kwargs: Any) -> "QuerySet[T]":
        if len(args) == 1:
            filter = args[0]
        elif len(args) == 0 and len(kwargs) > 0:
            filter = lambda obj: all(
                getattr(obj, key) == value for key, value in kwargs.items()
            )
        else:
            raise TypeError("filter() and get() expect either a callable or **kwargs")

        qs = QuerySet(self._data)
        qs._filters = self._filters.copy() + [filter]
        return qs

    @overload
    def get(self, match: Callable[[T], Any]) -> Optional[T]:
        ...

    @overload
    def get(self, **kwargs: Any) -> Optional[T]:
        ...

    def get(self, *args: Callable[[T], Any], **kwargs: Any) -> Optional[T]:
        return next(iter(self.filter(*args, **kwargs)), None)
