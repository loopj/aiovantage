"""Thermostat object."""

from dataclasses import dataclass, field
from enum import IntEnum

from .station_object import StationObject


@dataclass(kw_only=True)
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

    # State
    operation_mode: OperationMode | None = field(
        default=None, metadata={"type": "Ignore"}
    )
    fan_mode: FanMode | None = field(default=None, metadata={"type": "Ignore"})
    day_mode: DayMode | None = field(default=None, metadata={"type": "Ignore"})
    hold_mode: HoldMode | None = field(default=None, metadata={"type": "Ignore"})
    status: Status | None = field(default=None, metadata={"type": "Ignore"})
