from collections.abc import Callable, Collection, Iterator
from typing import Any, Generic, TypeVar, overload

T = TypeVar("T")


class QuerySet(Generic[T]):
    _data: Collection[T]

    def __init__(self, data: Collection[T]) -> None:
        self._data = data

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

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
            return QuerySet([obj for obj in self._data if args[0](obj)])

        if len(args) == 0 and len(kwargs) > 0:
            return QuerySet(
                [
                    obj
                    for obj in self._data
                    if all(getattr(obj, key) == value for key, value in kwargs.items())
                ]
            )

        raise TypeError("filter() and get() expect either a callable or **kwargs")

    @overload
    def get(self, match: Callable[[T], Any]) -> T | None:
        ...

    @overload
    def get(self, **kwargs: Any) -> T | None:
        ...

    def get(self, *args: Callable[[T], Any], **kwargs: Any) -> T | None:
        return next(iter(self.filter(*args, **kwargs)), None)
