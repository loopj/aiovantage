"""Temperature object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import TemperatureInterface

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class Temperature(Sensor, TemperatureInterface):
    """Temperature object."""

    parent: Parent
    out_of_range: int = 0
    in_range: int = 0
    range_high: float
    range_low: float
    hold_on_time: float
    temp: int = 0
