"""Base class for system objects in an area."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass(kw_only=True)
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    # Some objects in firmware 2.x do not have an area_id or location

    area: int | None = None
    location: str | None = None
