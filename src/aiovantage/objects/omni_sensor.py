"""OmniSensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from types import NoneType

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

    async def get_level(self) -> Decimal:
        """Get the value of the OmniSensor object, using cached value if available.

        Returns:
            The level of the sensor.
        """
        return await self.invoke(self.get.method, as_type=Decimal)

    async def get_level_hw(self) -> Decimal:
        """Get the value of the OmniSensor object directly from the hardware.

        Returns:
            The level of the sensor.
        """
        return await self.invoke(self.get.method_hw, as_type=Decimal)

    async def set_level(self, level: Decimal) -> None:
        """Set the value of the OmniSensor object.

        Args:
            level: The value to set the sensor to.
        """
        await self.invoke(self.set.method, level, as_type=NoneType)

    async def set_level_sw(self, level: Decimal) -> None:
        """Set the cached value of the OmniSensor object.

        Args:
            level: The value to set the sensor to.
        """
        await self.invoke(self.set.method_sw, level, as_type=NoneType)

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
