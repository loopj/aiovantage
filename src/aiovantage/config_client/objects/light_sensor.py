"""Light sensor object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .sensor import Sensor


@dataclass
class LightSensor(Sensor):
    """Light sensor object."""

    def __post_init__(self) -> None:
        self.level: Optional[Decimal] = None
