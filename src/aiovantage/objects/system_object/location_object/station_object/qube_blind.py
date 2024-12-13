"""Qube blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface

from . import StationObject


@dataclass
class QubeBlind(StationObject, BlindInterface):
    """Qube blind object."""
