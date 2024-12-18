"""Thermostat object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ThermostatInterface

from .station_object import StationObject


@dataclass
class Thermostat(StationObject, ThermostatInterface):
    """Thermostat object."""
