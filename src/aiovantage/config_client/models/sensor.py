"""Sensor object."""

from attr import define

from .location_object import LocationObject


@define
class Sensor(LocationObject):
    """Sensor object."""
