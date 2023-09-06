"""Thermostat object."""
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

from .station_object import StationObject


@dataclass
class Thermostat(StationObject):
    """Thermostat object."""

    class OperationMode(IntEnum):
        """The operation mode of the thermostat."""

        OFF = 0
        COOL = 1
        HEAT = 2
        AUTO = 3

    class FanMode(IntEnum):
        """The fan mode of the thermostat."""

        AUTO = 0
        ON = 1

    class DayMode(IntEnum):
        """The day mode of the thermostat."""

        DAY = 0
        NIGHT = 1

    class HoldMode(IntEnum):
        """The hold mode of the thermostat."""

        NORMAL = 0
        HOLD = 1

    class Status(IntEnum):
        """The status of the thermostat."""

        OFF = 0
        COOLING = 1
        HEATING = 2
        OFFLINE = 3

    operation_mode: Optional[OperationMode] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    fan_mode: Optional[FanMode] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    day_mode: Optional[DayMode] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    hold_mode: Optional[HoldMode] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    # Not available in 2.x firmware
    status: Optional[Status] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
