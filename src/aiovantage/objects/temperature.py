"""Temperature object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

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

    # Not available in 2.x firmware
    setpoint: Setpoint | None = field(default=None, metadata={"type": "Attribute"})
    parent: Parent

    # State
    value: Decimal | None = field(default=None, metadata={"type": "Ignore"})
