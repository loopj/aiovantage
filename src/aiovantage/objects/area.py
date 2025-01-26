"""Area object."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass(kw_only=True)
class Area(LocationObject):
    """Area object."""
