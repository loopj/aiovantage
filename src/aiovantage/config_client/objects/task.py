"""Task object."""

from dataclasses import dataclass
from typing import Optional

from .system_object import SystemObject


@dataclass
class Task(SystemObject):
    """Task object."""

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.is_running: Optional[bool] = None
        self.state: Optional[bool] = None
