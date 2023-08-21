"""Light sensor object."""

from decimal import Decimal
from typing import Optional

from attr import define, field

from .sensor import Sensor
from .types import Parent


@define
class LightSensor(Sensor):
    """Light sensor object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    level: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
