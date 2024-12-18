"""Task object."""

from dataclasses import dataclass, field

from .system_object import SystemObject


@dataclass
class Task(SystemObject):
    """Task object."""

    # State
    is_running: bool | None = field(default=None, metadata={"type": "Ignore"})
    state: int | None = field(default=None, metadata={"type": "Ignore"})
