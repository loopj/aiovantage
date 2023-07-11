"""Task object."""

from dataclasses import dataclass, field
from typing import Optional

from .system_object import SystemObject


@dataclass
class Task(SystemObject):
    """Task object."""

    is_running: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    state: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
