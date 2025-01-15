"""Base class for system objects in an area."""

from dataclasses import dataclass

from .system_object import SystemObject


@dataclass(kw_only=True)
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    area: int
    location: str
