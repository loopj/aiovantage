"""Thermostat object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import ThermostatInterface

from .station_object import StationObject


@dataclass(kw_only=True)
class Thermostat(StationObject, ThermostatInterface):
    """Thermostat object."""

    day_mode_event: int = field(default=0, metadata={"name": "DayMode"})
    fan_mode_event: int = field(default=0, metadata={"name": "FanMode"})
    operation_mode_event: int = field(default=0, metadata={"name": "OperationMode"})
    external_temperature: int
    display_clock: bool = True
    pseudo_mode: bool = True
    humidistat: bool = False
