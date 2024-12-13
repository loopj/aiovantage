"""Area object."""

from dataclasses import dataclass

from aiovantage.objects.location_object import LocationObject


@dataclass
class Area(LocationObject):
    """Area object."""
