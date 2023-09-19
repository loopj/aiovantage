"""IIntrospection.GetTypes method definition."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Type:
    """Object type definition."""

    name: str = field(metadata={"name": "Name"})
    version: str = field(metadata={"name": "Version"})


@dataclass
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call = None
    return_value: list[Type] | None = field(
        default=None,
        metadata={
            "name": "Type",
            "wrapper": "return",
        },
    )
