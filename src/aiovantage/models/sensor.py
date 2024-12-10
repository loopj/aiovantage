"""Sensor object."""

from dataclasses import dataclass

from aiovantage.models.location_object import LocationObject

# NOTE: Firmware 2.x inherits from SystemObject, not LocationObject


@dataclass
class Sensor(LocationObject):
    """Sensor object."""
