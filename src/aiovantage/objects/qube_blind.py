"""Qube blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .station_object import StationObject


@dataclass
class QubeBlind(StationObject, BlindInterface):
    """Qube blind object."""
