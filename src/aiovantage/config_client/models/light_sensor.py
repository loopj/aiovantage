"""Light sensor object."""

from decimal import Decimal
from typing import Optional

from attr import define, field

from .child_object import ChildObject
from .sensor import Sensor


@define
class LightSensor(ChildObject, Sensor):
    """Light sensor object."""

    level: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
