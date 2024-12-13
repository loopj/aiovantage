"""OmniSensor object."""

from dataclasses import dataclass, field
from enum import Enum

from aiovantage.object_interfaces.sensor import SensorInterface
from aiovantage.objects.types import Parent

from . import Sensor


class ConversionType(Enum):
    """OmniSensor type conversion information."""

    FIXED = "fixed"
    INT = "int"


@dataclass(kw_only=True)
class OmniSensor(Sensor, SensorInterface):
    """OmniSensor object."""

    ConversionType = ConversionType

    @dataclass
    class GetMethodType:
        @dataclass
        class Formula:
            return_type: ConversionType = field(metadata={"type": "Attribute"})
            level_type: ConversionType = field(metadata={"type": "Attribute"})

        formula: Formula
        method: str
        method_hw: str = field(metadata={"name": "MethodHW"})

    parent: Parent
    get: GetMethodType

    @property
    def is_current_sensor(self) -> bool:
        """Return True if the sensor is a current sensor."""
        return self.model == "Current"

    @property
    def is_power_sensor(self) -> bool:
        """Return True if the sensor is a power sensor."""
        return self.model == "Power"

    @property
    def is_temperature_sensor(self) -> bool:
        """Return True if the sensor is a temperature sensor."""
        return self.model == "Temperature"
