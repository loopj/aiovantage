"""Thermostat object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface

from . import StationObject


@dataclass(kw_only=True)
class Thermostat(StationObject, ThermostatInterface):
    """Thermostat object."""
