"""Base class for custom device objects."""

from dataclasses import dataclass

from .. import LocationObject


@dataclass
class CustomDevice(LocationObject):
    """Base class for custom device objects."""
