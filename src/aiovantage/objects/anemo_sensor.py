"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import AnemoSensorInterface, SensorInterface

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class AnemoSensor(Sensor, SensorInterface, AnemoSensorInterface):
    """AnemoSensor (wind sensor) object."""

    parent: Parent
    out_of_range: int = 0
    in_range: int = 0
    range_high: float = 10.0
    range_low: float = 0.0
    hold_on_time: float
