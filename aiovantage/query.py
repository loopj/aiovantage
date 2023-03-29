from typing import Any, Callable, Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


class QuerySet(Generic[T]):
    _data: Iterable[T]

    def __init__(self, data: Iterable) -> None:
        self._data = data

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __bool__(self) -> bool:
        return any(self._data)

    def filter(
        self, *args: Optional[Callable[[T], bool]], **kwargs: Any
    ) -> "QuerySet[T]":
        if len(args) == 1 and callable(args[0]):
            return QuerySet(filter(args[0], self._data))
        elif len(kwargs) > 0:
            return QuerySet(
                (
                    obj
                    for obj in self._data
                    if all(getattr(obj, key) == value for key, value in kwargs.items())
                )
            )
        else:
            raise TypeError("filter() expects lambda or kwargs")

    def get(self, *args: Optional[Callable[[T], bool]], **kwargs: Any) -> Optional[T]:
        return next(iter(self.filter(*args, **kwargs)), None)
