"""IConfiguration.CloseFilter method definition."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class CloseFilter:
    """IConfiguration.CloseFilter method definition."""

    interface: ClassVar[str] = "IConfiguration"
    call: int | None = field(default=None)
    return_value: bool | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
