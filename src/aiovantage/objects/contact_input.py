"""Contact Input."""

from dataclasses import dataclass

from aiovantage.objects.station_object import StationObject


@dataclass
class ContactInput(StationObject):
    """Contact Input."""
