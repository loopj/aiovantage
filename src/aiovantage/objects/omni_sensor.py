"""OmniSensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from aiovantage.object_interfaces import SensorInterface

from .sensor import Sensor
from .types import Parent


class ConversionType(Enum):
    """Conversion type for OmniSensor formulas."""

    FIXED = "fixed"
    INT = "int"


@dataclass(kw_only=True)
class OmniSensor(Sensor, SensorInterface):
    """OmniSensor object."""

    @dataclass
    class Get:
        @dataclass(kw_only=True)
        class Formula:
            return_type: ConversionType = field(
                default=ConversionType.FIXED,
                metadata={"type": "Attribute"},
            )
            level_type: ConversionType = field(
                default=ConversionType.INT,
                metadata={"type": "Attribute"},
            )
            formula: str

        formula: Formula
        method: str
        method_hw: str = field(metadata={"name": "MethodHW"})

    @dataclass
    class Set:
        @dataclass(kw_only=True)
        class Formula:
            return_type: ConversionType = field(
                default=ConversionType.INT,
                metadata={"type": "Attribute"},
            )
            value_type: ConversionType = field(
                default=ConversionType.FIXED,
                metadata={"type": "Attribute"},
            )
            formula: str

        formula: Formula
        method: str
        method_sw: str = field(metadata={"name": "MethodSW"})

    parent: Parent
    get: Get
    set: Set

    async def get_level(self, use_cache: bool = False) -> Decimal:
        """Get the value of the OmniSensor object.

        Args:
            use_cache: Use the cached value if available.

        Returns:
            The level of the sensor.
        """
        # Determine which method to use
        method = self.get.method if use_cache else self.get.method_hw

        # Fetch the value
        return await self.invoke(method, as_type=Decimal)

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
