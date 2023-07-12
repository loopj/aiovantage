"""OmniSensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union

from .child_object import ChildObject
from .sensor import Sensor


@dataclass
class Formula:
    """OmniSensor type conversion information."""

    return_type: str = field(
        metadata={
            "name": "ReturnType",
            "type": "Attribute",
        }
    )

    level_type: str = field(
        metadata={
            "name": "LevelType",
            "type": "Attribute",
        }
    )


@dataclass
class GetMethodType:
    """Omnisensor method information."""

    formula: Formula = field(
        metadata={
            "name": "Formula",
        }
    )

    method: str = field(
        metadata={
            "name": "Method",
        }
    )

    method_hw: str = field(
        metadata={
            "name": "MethodHW",
        }
    )


@dataclass
class OmniSensor(ChildObject, Sensor):
    """OmniSensor object."""

    get: GetMethodType = field(
        metadata={
            "name": "Get",
        }
    )

    level: Union[int, Decimal, None] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

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
