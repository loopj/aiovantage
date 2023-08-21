"""IIntrospection.GetTypes method definition."""

from typing import ClassVar, List, Optional

from attr import define, field


@define
class Type:
    """Object type definition."""

    name: str = field(metadata={"name": "Name"})
    version: str = field(metadata={"name": "Version"})


@define
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    interface: ClassVar[str] = "IIntrospection"
    call: Optional[object] = field(default=None)
    return_value: Optional[List[Type]] = field(
        default=None,
        metadata={
            "name": "Type",
            "wrapper": "return",
        },
    )
