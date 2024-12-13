"""Base class for custom device objects."""

from dataclasses import dataclass

from aiovantage.objects.location_object import LocationObject


@dataclass
class CustomDevice(LocationObject):
    """Base class for custom device objects."""
