"""Duck typing for methods."""

from typing import Protocol, TypeVar

Call = TypeVar("Call")
Return = TypeVar("Return")


class Method(Protocol[Call, Return]):
    """Duck typing for methods."""

    interface: str
    call: Call | None
    return_value: Return | None
