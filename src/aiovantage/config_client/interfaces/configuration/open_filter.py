"""IConfiguration.OpenFilter method definition."""

from dataclasses import dataclass, field
from typing import ClassVar


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

    interface: ClassVar[str] = "IConfiguration"
    call: Params | None = field(default=None)
    return_value: int | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
