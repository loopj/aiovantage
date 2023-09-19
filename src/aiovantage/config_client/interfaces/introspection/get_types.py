"""IIntrospection.GetTypes method definition."""

from dataclasses import dataclass, field


@dataclass
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    interface = "IIntrospection"

    @dataclass
    class Type:
        """Object type definition."""

        name: str = field(metadata={"name": "Name"})
        version: str = field(metadata={"name": "Version"})

    call = None
    return_value: list[Type] | None = field(
        default=None,
        metadata={
            "name": "Type",
            "wrapper": "return",
        },
    )
