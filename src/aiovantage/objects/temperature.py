"""Temperature object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class Temperature(Sensor):
    """Temperature object."""

    parent: Parent
    out_of_range: int = 0
    in_range: int = 0
    range_high: float
    range_low: float
    hold_on_time: float
    temp: int = 0

    # Not available in 2.x firmware, not strictly in the schema
    class Setpoint(Enum):
        """Setpoint type."""

        HEAT = "Heat"
        COOL = "Cool"
        AUTO = "Auto"

    setpoint: Setpoint | None = field(default=None, metadata={"type": "Attribute"})

    # State
    value: Decimal | None = field(default=None, metadata={"type": "Ignore"})
