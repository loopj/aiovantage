"""RS-485 Station."""

from dataclasses import dataclass

from aiovantage.objects.station_object import StationObject


@dataclass
class RS485Station(StationObject):
    """RS-485 Station."""
