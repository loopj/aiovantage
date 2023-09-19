"""IConfiguration.GetFilterResults method definition."""

from dataclasses import dataclass, field
from typing import ClassVar

from aiovantage.config_client.interfaces.types import ObjectChoice


@dataclass
class GetFilterResults:
    """IConfiguration.GetFilterResults method definition."""

    @dataclass
    class Params:
        """IConfiguration.GetFilterResults method parameters."""

        h_filter: int = field(
            metadata={
                "name": "hFilter",
            }
        )

        count: int = field(
            default=50,
            metadata={
                "name": "Count",
            },
        )

        whole_object: bool = field(
            default=True,
            metadata={
                "name": "WholeObject",
            },
        )

    interface: ClassVar[str] = "IConfiguration"
    call: Params | None = field(default=None)
    return_value: list[ObjectChoice] | None = field(
        default=None,
        metadata={
            "name": "Object",
            "wrapper": "return",
        },
    )
