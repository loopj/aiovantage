"""Area object."""

from dataclasses import dataclass

from aiovantage.models.location_object import LocationObject


@dataclass
class Area(LocationObject):
    """Area object."""
