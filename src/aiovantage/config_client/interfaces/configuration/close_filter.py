"""IConfiguration.CloseFilter method definition."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional


@dataclass
class CloseFilter:
    """IConfiguration.CloseFilter method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: Optional[int] = field(default=None)
    return_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
