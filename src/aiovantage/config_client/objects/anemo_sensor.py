"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .child_object import ChildObject
from .sensor import Sensor


@dataclass
class AnemoSensor(Sensor, ChildObject):
    """AnemoSensor (wind sensor) object."""

    speed: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
