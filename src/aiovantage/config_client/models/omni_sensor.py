"""OmniSensor object."""

from decimal import Decimal
from enum import Enum
from typing import Union

from attr import define, field

from .sensor import Sensor
from .types import Parent


class ConversionType(Enum):
    """OmniSensor type conversion information."""

    FIXED = "fixed"
    INT = "int"


@define
class Formula:
    """OmniSensor conversion formula information."""

    return_type: ConversionType = field(
        metadata={
            "name": "ReturnType",
            "type": "Attribute",
        }
    )

    level_type: ConversionType = field(
        metadata={
            "name": "LevelType",
            "type": "Attribute",
        }
    )

    value: str


@define
class GetMethodType:
    """Omnisensor get method information."""

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


@define
class OmniSensor(Sensor):
    """OmniSensor object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

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
