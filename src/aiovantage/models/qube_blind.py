"""Qube blind object."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class QubeBlind(StationObject, BlindInterface):
    """Qube blind object."""
