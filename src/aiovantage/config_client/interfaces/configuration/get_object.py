"""IConfiguration.GetObject method definition."""

from dataclasses import dataclass, field
from typing import ClassVar

from aiovantage.config_client.interfaces.types import ObjectChoice


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    @dataclass
    class Params:
        """IConfiguration.GetObject method parameters."""

        vids: list[int] = field(
            metadata={
                "name": "VID",
            }
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
