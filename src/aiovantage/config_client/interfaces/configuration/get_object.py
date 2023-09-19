"""IConfiguration.GetObject method definition."""

from dataclasses import dataclass, field

from aiovantage.config_client.interfaces.types import ObjectChoice


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    interface = "IConfiguration"

    @dataclass
    class Params:
        """Method parameters."""

        vids: list[int] = field(
            metadata={
                "name": "VID",
            }
        )

    call: Params | None = field(default=None)
    return_value: list[ObjectChoice] | None = field(
        default=None,
        metadata={
            "name": "Object",
            "wrapper": "return",
        },
    )
