"""Equinox 41 or Equinox 73 touchscreen."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject


@dataclass
class EqUX(StationObject):
    """Equinox 41 or Equinox 73 touchscreen."""
