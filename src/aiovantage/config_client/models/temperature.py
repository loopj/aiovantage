"""Temperature object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class Temperature(Sensor):
    """Temperature object."""

    class Setpoint(Enum):
        """Setpoint type."""

        HEAT = "Heat"
        COOL = "Cool"
        AUTO = "Auto"

    setpoint: Optional[Setpoint] = field(
        default=None,
        metadata={
            "name": "Setpoint",
            "type": "Attribute",
        },
    )

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
