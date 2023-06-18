"""Duck typing for methods."""

from typing import ClassVar, Optional, Protocol, TypeVar

Call = TypeVar("Call")
Return = TypeVar("Return")


class Method(Protocol[Call, Return]):
    """Duck typing for methods."""

    interface: ClassVar[str]
    call: Optional[Call]
    return_value: Optional[Return]
