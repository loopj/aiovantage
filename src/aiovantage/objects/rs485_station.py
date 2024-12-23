"""RS-485 Station."""

from dataclasses import dataclass

from .station_object import StationObject


@dataclass(kw_only=True)
class RS485Station(StationObject):
    """RS-485 Station."""
