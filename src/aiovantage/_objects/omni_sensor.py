"""OmniSensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from types import NoneType

from typing_extensions import override

from aiovantage.command_client import Converter
from aiovantage.object_interfaces import SensorInterface

from .sensor import Sensor
from .types import Parent


class ConversionType(Enum):
    """OmniSensor type conversion information."""

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

    async def get_level(self, *, hw: bool = False) -> Decimal:
        """Get the value of the OmniSensor object, using cached value if available.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The level of the sensor.
        """
        return await self.invoke(
            self.get.method_hw if hw else self.get.method, as_type=Decimal
        )

    async def set_level(self, level: Decimal, *, sw: bool = False) -> None:
        """Set the value of the OmniSensor object.

        Args:
            level: The value to set the sensor to.
            sw: Set the cached value instead of the hardware value.
        """
        await self.invoke(
            self.set.method_sw if sw else self.set.method, level, as_type=NoneType
        )

    # NOTE: We are explicitly _not_ calling the parent methods in fetch_state and
    # handle_object_status, as we don't want SensorInterface to handle the state.
    # OmniSensors do additional conversion behind the scenes.

    @override
    async def fetch_state(self) -> list[str]:
        return self.update_properties({"level": await self.get_level(hw=True)})

    @override
    def handle_object_status(self, method: str, result: str, *args: str) -> list[str]:
        # Check if the method is one we're interested in
        if method != self.get.method:
            return []

        # Update the property if it has changed
        return self.update_properties({"level": Converter.deserialize(Decimal, result)})
