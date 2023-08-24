"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .sensor import Sensor
from .types import Parent


@dataclass
class AnemoSensor(Sensor):
    """AnemoSensor (wind sensor) object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    speed: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
