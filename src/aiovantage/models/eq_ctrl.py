"""Equinox 40 Station."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject
from aiovantage.object_interfaces import SounderInterface


@dataclass
class EqCtrl(StationObject, SounderInterface):
    """Equinox 40 Station."""
