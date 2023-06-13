from dataclasses import dataclass
from typing import Optional

from .location_object import LocationObject


@dataclass
class Sensor(LocationObject):
    def __post_init__(self) -> None:
        self.level: Optional[int] = None
