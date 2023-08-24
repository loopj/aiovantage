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

        Off = 0
        Cool = 1
        Heat = 2
        Auto = 3
        Unknown = 4

    class FanMode(IntEnum):
        """The fan mode of the thermostat."""

        Off = 0
        On = 1
        Unknown = 2

    class DayMode(IntEnum):
        """The day mode of the thermostat."""

        Day = 0
        Night = 1
        Unknown = 2
        Standby = 3

    class HoldMode(IntEnum):
        """The hold mode of the thermostat."""

        Normal = 0
        Hold = 1
        Unknown = 2

    class Status(IntEnum):
        """The status of the thermostat."""

        Off = 0
        Cooling = 1
        Heating = 2
        Offline = 3

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

    status: Optional[Status] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
