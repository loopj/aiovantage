"""Temperature object."""

from dataclasses import dataclass, field
from enum import Enum

from aiovantage.object_interfaces.temperature import TemperatureInterface
from aiovantage.objects.types import Parent

from . import Sensor


class Setpoint(Enum):
    """Setpoint type."""

    HEAT = "Heat"
    COOL = "Cool"
    AUTO = "Auto"


@dataclass(kw_only=True)
class Temperature(Sensor, TemperatureInterface):
    """Temperature object."""

    # setpoint not available in 2.x firmware

    setpoint: Setpoint | None = field(default=None, metadata={"type": "Attribute"})
    parent: Parent
