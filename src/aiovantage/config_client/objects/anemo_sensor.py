"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .sensor import Sensor


@dataclass
class AnemoSensor(Sensor):
    """AnemoSensor (wind sensor) object."""

    def __post_init__(self) -> None:
        self.speed: Optional[Decimal] = None
