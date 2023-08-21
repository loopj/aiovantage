"""Task object."""

from typing import Optional

from attr import define, field

from .system_object import SystemObject


@define
class Task(SystemObject):
    """Task object."""

    is_running: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    state: Optional[int] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
