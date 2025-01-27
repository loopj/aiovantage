"""IConfiguration.GetFilterResults method definition."""

from dataclasses import dataclass, field


@dataclass
class GetFilterResults:
    """IConfiguration.GetFilterResults method definition."""

    interface = "IConfiguration"

    @dataclass
    class Params:
        """Method parameters."""

        h_filter: int = field(metadata={"name": "hFilter"})
        count: int = 50
        whole_object: bool = True

    @dataclass
    class Object:
        """Wildcard type that can be used to represent any object."""

        vid: int = field(metadata={"name": "VID", "type": "Attribute"})
        obj: object = field(metadata={"type": "Wildcard"})

    call: Params | None = field(
        default=None,
        metadata={
            "name": "call",
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
