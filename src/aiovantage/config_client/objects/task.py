from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .system_object import SystemObject


@dataclass
class Task(SystemObject):
    class EventType(Enum):
        CANCEL = -2
        NONE = -1
        RELEASE = 0
        PRESS = 1
        HOLD = 2
        TIMER = 3
        DATA = 4
        POSITION = 5
        INRANGE = 6
        OUTOFRANGE = 7
        TEMPERATURE = 8
        DAYMODE = 9
        FANMODE = 10
        OPERATIONMODE = 11
        CONNECT = 12
        DISCONNECT = 13
        BOOT = 14
        LEARN = 15

    def __post_init__(self) -> None:
        self.is_running: Optional[bool] = None
        self.state: Optional[bool] = None
