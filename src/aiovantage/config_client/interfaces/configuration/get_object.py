"""IConfiguration.GetObject method definition."""

from typing import ClassVar, List, Optional

from attr import define, field

from aiovantage.config_client.interfaces.types import ObjectChoice


@define
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

    @define
    class Params:
        """IConfiguration.GetObject method parameters."""

        vids: List[int] = field(
            metadata={
                "name": "VID",
            }
        )
