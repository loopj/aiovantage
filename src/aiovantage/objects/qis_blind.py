"""QIS Shade object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .station_object import StationObject


@dataclass(kw_only=True)
class QISBlind(StationObject, BlindInterface):
    """QIS Shade object."""

    @dataclass
    class Movement:
        open: float = 5.0
        close: float = 5.0

    upper_limit: float
    lower_limit: float
    movement: Movement
