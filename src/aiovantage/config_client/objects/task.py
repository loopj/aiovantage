from dataclasses import dataclass
from typing import Optional

from .system_object import SystemObject


@dataclass
class Task(SystemObject):
    def __post_init__(self) -> None:
        self.is_running: Optional[bool] = None
        self.state: Optional[bool] = None
