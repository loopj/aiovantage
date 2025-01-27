"""IConfiguration.GetObject method definition."""

from dataclasses import dataclass, field


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    interface = "IConfiguration"

    @dataclass
    class Object:
        """Wildcard type that can be used to represent any object."""

        vid: int = field(metadata={"name": "VID", "type": "Attribute"})
        obj: object = field(metadata={"type": "Wildcard"})

    call: list[int] | None = field(
        default=None,
        metadata={
            "wrapper": "call",
            "name": "VID",
            "type": "Element",
        },
    )

    result: list[Object] | None = field(
        default=None,
        metadata={
            "wrapper": "return",
            "name": "Object",
            "type": "Element",
        },
    )
