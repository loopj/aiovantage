from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CloseFilter:
    call: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    return_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )
