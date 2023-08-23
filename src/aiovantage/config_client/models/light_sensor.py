"""Light sensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .sensor import Sensor
from .types import Parent


@dataclass
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
