from typing import ClassVar, Optional, Protocol, TypeVar

CallType = TypeVar("CallType")
ReturnType = TypeVar("ReturnType")


class Method(Protocol[CallType, ReturnType]):
    """Duck typing for methods"""

    interface: ClassVar[str]
    call: Optional[CallType]
    return_value: Optional[ReturnType]
