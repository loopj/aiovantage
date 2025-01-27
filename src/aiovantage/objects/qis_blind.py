"""QIS Shade object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .station_object import StationObject


@dataclass(kw_only=True)
class QISBlind(BlindBase, StationObject):
    """QIS Shade object."""

    @dataclass
    class Movement:
        open: float = 5.0
        close: float = 5.0

    upper_limit: float
    lower_limit: float
    movement: Movement
