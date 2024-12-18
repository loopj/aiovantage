"""Light sensor object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import LightSensorInterface, SensorInterface

from .sensor import Sensor
from .types import Parent


@dataclass
class LightSensor(Sensor, LightSensorInterface, SensorInterface):
    """Light sensor object."""

    parent: Parent
