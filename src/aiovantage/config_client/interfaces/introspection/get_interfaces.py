"""IIntrospection.GetInterfaces method definition."""

from typing import ClassVar, List, Optional

from attr import define, field


@define
class Interface:
    """Object interface definition."""

    name: str = field(metadata={"name": "Name"})
    version: str = field(metadata={"name": "Version"})
    id: int = field(metadata={"name": "IID"})


@define
class GetInterfaces:
    """IIntrospection.GetInterfaces method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: Optional[List[Interface]] = field(
        default=None,
        metadata={
            "name": "Interface",
            "wrapper": "return",
        },
    )
