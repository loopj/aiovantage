"""Base class for system objects in an area."""

from dataclasses import dataclass, field

from .system_object import SystemObject


@dataclass
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
