"""Qube blind object."""

from attr import define

from .blind_base import BlindBase
from .station_object import StationObject


@define
class QubeBlind(BlindBase, StationObject):
    """Qube blind object."""
