"""Qube blind object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .station_object import StationObject


@dataclass(kw_only=True)
class QubeBlind(BlindBase, StationObject):
    """Qube blind object."""
