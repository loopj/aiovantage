"""IConfiguration.GetFilterResults method definition."""

from dataclasses import dataclass, field

from aiovantage.config_client.interfaces.types import ObjectChoice


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

    call: Params | None = field(
        default=None,
        metadata={
            "name": "call",
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
