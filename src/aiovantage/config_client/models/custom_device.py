"""Base class for custom device objects."""

from attr import define

from .location_object import LocationObject


@define
class CustomDevice(LocationObject):
    """Base class for custom device objects."""
