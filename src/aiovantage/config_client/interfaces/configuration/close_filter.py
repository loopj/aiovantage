"""IConfiguration.CloseFilter method definition."""

from dataclasses import dataclass, field


@dataclass
class CloseFilter:
    """IConfiguration.CloseFilter method definition."""

    interface = "IConfiguration"
    call: int | None = field(default=None)
    return_value: bool | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )
