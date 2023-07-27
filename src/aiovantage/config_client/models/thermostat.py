"""Thermostat object."""
from dataclasses import dataclass

from .station_object import StationObject


@dataclass
class Thermostat(StationObject):
    """Thermostat object."""
