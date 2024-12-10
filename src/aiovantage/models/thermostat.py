"""Thermostat object."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject
from aiovantage.object_interfaces.thermostat import ThermostatInterface


@dataclass
class Thermostat(StationObject, ThermostatInterface):
    """Thermostat object."""
