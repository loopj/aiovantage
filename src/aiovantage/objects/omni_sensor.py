"""OmniSensor object."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from .sensor import Sensor
from .types import Parent


class ConversionType(Enum):
    """OmniSensor type conversion information."""

    FIXED = "fixed"
    INT = "int"


@dataclass
class OmniSensor(Sensor):
    """OmniSensor object."""

    @dataclass
    class Get:
        @dataclass
        class Formula:
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

            formula: str

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

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    get: Get = field(
        metadata={
            "name": "Get",
        }
    )

    level: int | Decimal | None = field(
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
