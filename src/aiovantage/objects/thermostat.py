"""Thermostat object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface
from aiovantage.objects.station_object import StationObject


@dataclass
class Thermostat(StationObject, ThermostatInterface):
    """Thermostat object."""
