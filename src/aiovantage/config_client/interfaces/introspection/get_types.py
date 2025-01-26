"""IIntrospection.GetTypes method definition."""

from dataclasses import dataclass, field


@dataclass
class GetTypes:
    """IIntrospection.GetTypes method definition."""

    interface = "IIntrospection"

    @dataclass
    class Type:
        """Object type definition."""

        name: str
        version: str

    call = None

    result: list[Type] | None = field(
        default=None,
        metadata={
            "wrapper": "return",
            "name": "Type",
            "type": "Element",
        },
    )
