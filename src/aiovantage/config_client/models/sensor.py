"""Sensor object."""

from attr import define

from .location_object import LocationObject

# NOTE: Firmware 2.x inherits from SystemObject, not LocationObject


@define
class Sensor(LocationObject):
    """Sensor object."""
