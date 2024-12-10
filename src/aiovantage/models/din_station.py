"""Base class for DIN station objects."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject


@dataclass
class DINStation(StationObject):
    """Base class for DIN station objects."""
