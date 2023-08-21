"""Base class for all station objects."""

from attr import define, field

from .location_object import LocationObject


@define(slots=False)
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
