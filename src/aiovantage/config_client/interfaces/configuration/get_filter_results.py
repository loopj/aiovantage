"""IConfiguration.GetFilterResults method definition."""

from typing import ClassVar, List, Optional

from attr import define, field

from aiovantage.config_client.interfaces.types import ObjectChoice


@define
class GetFilterResults:
    """IConfiguration.GetFilterResults method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional["GetFilterResults.Params"] = field(default=None)
    return_value: Optional[List[ObjectChoice]] = field(
        default=None,
        metadata={
            "name": "Object",
            "wrapper": "return",
        },
    )

    @define
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
