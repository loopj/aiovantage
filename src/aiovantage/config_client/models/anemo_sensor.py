"""AnemoSensor (wind sensor) object."""

from decimal import Decimal
from typing import Optional

from attr import define, field

from .sensor import Sensor
from .types import Parent


@define
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
