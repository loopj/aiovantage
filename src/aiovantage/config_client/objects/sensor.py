"""Sensor object."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass
class Sensor(LocationObject):
    """Sensor object."""
