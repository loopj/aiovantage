"""Qz Shade object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .station_object import StationObject


@dataclass(kw_only=True)
class QubeBlind(BlindBase, StationObject):
    """Qz Shade object."""

    @dataclass
    class Movement:
        open: float = 5.0
        close: float = 5.0

    upper_limit: float
    lower_limit: float
    movement: Movement
    alert: int = 0
    low_battery_threshold: float = 20.0
