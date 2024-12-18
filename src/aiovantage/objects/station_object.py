"""Base class for all station objects."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass
class StationObject(LocationObject):
    """Base class for all station objects."""

    serial_number: str
    bus: int
