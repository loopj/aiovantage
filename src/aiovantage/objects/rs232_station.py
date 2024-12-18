"""RS-232 Station."""

from dataclasses import dataclass

from .station_object import StationObject


@dataclass
class RS232Station(StationObject):
    """RS-232 Station."""
