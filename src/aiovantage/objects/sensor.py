"""Sensor object."""

from dataclasses import dataclass

from aiovantage.objects.location_object import LocationObject

# NOTE: Firmware 2.x inherits from SystemObject, not LocationObject


@dataclass
class Sensor(LocationObject):
    """Sensor object."""
