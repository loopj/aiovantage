"""Base class for all station objects."""

from dataclasses import dataclass, field

from .location_object import LocationObject


@dataclass
class StationObject(LocationObject):
    """Base class for all station objects."""

    serial_number: str = field(
        metadata={
            "name": "SerialNumber",
        }
    )

    bus_id: int = field(
        metadata={
            "name": "Bus",
        }
    )
