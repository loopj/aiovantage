"""Temperature object."""

from dataclasses import dataclass, field
from enum import Enum

from aiovantage.object_interfaces import TemperatureInterface

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class Temperature(Sensor, TemperatureInterface):
    """Temperature object."""

    # TODO: Use a different approach to determine the setpoint type
    class Setpoint(Enum):
        HEAT = "Heat"
        COOL = "Cool"
        AUTO = "Auto"

    # Setpoint property not present in 2.x firmware
    setpoint: Setpoint | None = field(default=None, metadata={"type": "Attribute"})
    parent: Parent
