"""Temperature object."""

from dataclasses import dataclass, field
from enum import Enum

from aiovantage.object_interfaces.temperature import TemperatureInterface
from aiovantage.objects.types import Parent

from . import Sensor


@dataclass(kw_only=True)
class Temperature(Sensor, TemperatureInterface):
    """Temperature object."""

    class Setpoint(Enum):
        """Setpoint type."""

        HEAT = "Heat"
        COOL = "Cool"
        AUTO = "Auto"

    # Not available in 2.x firmware
    setpoint: Setpoint | None = field(
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
