"""IConfiguration.CloseFilter method definition."""

from typing import ClassVar, Optional

from attr import define, field


@define
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
