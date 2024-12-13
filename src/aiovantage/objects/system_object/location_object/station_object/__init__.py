"""Base class for all station objects."""

from dataclasses import dataclass

from .. import LocationObject


@dataclass(kw_only=True)
class StationObject(LocationObject):
    """Base class for all station objects."""

    serial_number: str
    bus: int
