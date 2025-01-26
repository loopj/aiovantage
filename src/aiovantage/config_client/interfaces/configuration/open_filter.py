"""IConfiguration.OpenFilter method definition."""

from dataclasses import dataclass, field


@dataclass
class OpenFilter:
    """IConfiguration.OpenFilter method definition."""

    interface = "IConfiguration"

    @dataclass
    class Params:
        """Method parameters."""

        object_types: list[str] | None = field(
            default=None,
            metadata={
                "wrapper": "Objects",
                "name": "ObjectType",
                "type": "Element",
            },
        )

        xpath: str | None = field(
            default=None,
            metadata={
                "name": "XPath",
            },
        )

    call: Params | None = field(
        default=None,
        metadata={
            "name": "call",
        },
    )

    result: int | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
