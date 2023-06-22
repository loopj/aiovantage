"""Duck typing for methods."""

from typing import ClassVar, Optional, Protocol, TypeVar

Call = TypeVar("Call")
Return = TypeVar("Return")


# TODO: Type variable "Call" used in generic protocol "Method" should be covariant
class Method(Protocol[Call, Return]):
    """Duck typing for methods."""

    interface: ClassVar[str]
    call: Optional[Call]
    return_value: Optional[Return]
