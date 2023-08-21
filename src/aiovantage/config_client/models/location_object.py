"""Base class for system objects in an area."""

from attr import define, field

from .system_object import SystemObject


@define(slots=False)
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    area_id: int = field(
        metadata={
            "name": "Area",
        }
    )

    location: str = field(
        metadata={
            "name": "Location",
        }
    )
