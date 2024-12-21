"""Contact Input."""

from dataclasses import dataclass

from .station_object import StationObject


@dataclass(kw_only=True)
class ContactInput(StationObject):
    """Contact Input."""
