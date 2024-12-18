"""Base class for custom device (driver provided) objects."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass
class CustomDevice(LocationObject):
    """Base class for custom device (driver provided) objects."""
