"""Base class for DIN station objects."""

from dataclasses import dataclass

from .station_object import StationObject


@dataclass(kw_only=True)
class DINStation(StationObject):
    """Base class for DIN station objects."""
