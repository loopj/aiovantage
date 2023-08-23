"""IIntrospection.GetTypes method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional


@dataclass
class Type:
    """Object type definition."""

    name: str = field(metadata={"name": "Name"})
    version: str = field(metadata={"name": "Version"})


@dataclass
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call: Optional[str] = field(default=None)
    return_value: Optional[List[Type]] = field(
        default=None,
        metadata={
            "name": "Type",
            "wrapper": "return",
        },
    )
