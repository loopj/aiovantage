"""IConfiguration.GetObject method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional

from aiovantage.config_client.methods.types import ObjectChoice


@dataclass
class GetObject:
    """IConfiguration.GetObject method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional["GetObject.Params"] = field(default=None)
    return_value: Optional[List[ObjectChoice]] = field(
        default=None,
        metadata={
            "name": "Object",
            "wrapper": "return",
        },
    )

    @dataclass
    class Params:
        """IConfiguration.GetObject method parameters."""

        vids: List[int] = field(
            metadata={
                "name": "VID",
            }
        )
