"""IConfiguration.GetObject method definition."""

from dataclasses import dataclass, field

from aiovantage.config_client.interfaces.types import ObjectChoice


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    interface = "IConfiguration"

    call: list[int] | None = field(
        default=None,
        metadata={
            "wrapper": "call",
            "name": "VID",
            "type": "Element",
        },
    )

    result: list[ObjectChoice] | None = field(
        default=None,
        metadata={
            "wrapper": "return",
            "name": "Object",
            "type": "Element",
        },
    )
