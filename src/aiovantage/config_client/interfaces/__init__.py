"""Duck typing for methods."""

from typing import ClassVar, Protocol, TypeVar

Call = TypeVar("Call")
Return = TypeVar("Return")


class Method(Protocol[Call, Return]):
    """Duck typing for methods."""

    interface: ClassVar[str]
    call: Call | None
    return_value: Return | None
