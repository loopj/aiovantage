"""IConfiguration.OpenFilter method definition."""

from dataclasses import dataclass, field


@dataclass
class OpenFilter:
    """IConfiguration.OpenFilter method definition."""

    @dataclass
    class Params:
        """IConfiguration.OpenFilter method parameters."""

        object_types: list[str] | None = field(
            default=None,
            metadata={
                "name": "ObjectType",
                "wrapper": "Objects",
            },
        )

        xpath: str | None = field(
            default=None,
            metadata={
                "name": "XPath",
            },
        )

    interface = "IConfiguration"
    call: Params | None = field(default=None)
    return_value: int | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
