"""IConfiguration.GetFilterResults method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional

from aiovantage.config_client.methods.types import ObjectChoice


@dataclass
class GetFilterResults:
    """IConfiguration.GetFilterResults method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional["GetFilterResults.Params"] = field(default=None)
    return_value: Optional[List[ObjectChoice]] = field(
        default=None, metadata={"name": "Object", "wrapper": "return"}
    )

    @dataclass
    class Params:
        """IConfiguration.GetFilterResults method parameters."""

        h_filter: int = field(metadata={"name": "hFilter"})
        count: int = field(default=50, metadata={"name": "Count"})
        whole_object: bool = field(default=True, metadata={"name": "WholeObject"})
