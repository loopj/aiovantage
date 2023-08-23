"""IIntrospection.GetInterfaces method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional


@dataclass
class Interface:
    """Object interface definition."""

    name: str = field(metadata={"name": "Name"})
    version: str = field(metadata={"name": "Version"})
    id: int = field(metadata={"name": "IID"})


@dataclass
class GetInterfaces:
    """IIntrospection.GetInterfaces method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call: Optional[str] = field(default=None)
    return_value: Optional[List[Interface]] = field(
        default=None,
        metadata={
            "name": "Interface",
            "wrapper": "return",
        },
    )
