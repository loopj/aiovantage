"""OmniSensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from .sensor import Sensor
from .types import Parent


@dataclass
class OmniSensor(Sensor):
    """OmniSensor object."""

    class ConversionType(Enum):
        FIXED = "fixed"
        INT = "int"

    @dataclass
    class Get:
        """Omnisensor get method information."""

        @dataclass
        class Formula:
            return_type: "OmniSensor.ConversionType" = field(
                metadata={"type": "Attribute"}
            )
            level_type: "OmniSensor.ConversionType" = field(
                metadata={"type": "Attribute"}
            )
            value: str

        formula: Formula
        method: str
        method_hw: str = field(metadata={"name": "MethodHW"})

    parent: Parent
    get: Get

    # State
    level: int | Decimal | None = field(default=None, metadata={"type": "Ignore"})

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
