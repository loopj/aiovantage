"""Base class for system objects in an area."""

from dataclasses import dataclass, field

from .system_object import SystemObject


@dataclass(kw_only=True)
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    # Some objects in firmware 2.x do not have an area_id
    area: int | None = field(
        default=None,
        metadata={
            "name": "Area",
        },
    )

    # Some objects in firmware 2.x do not have a location
    location: str | None = field(
        default=None,
        metadata={
            "name": "Location",
        },
    )
