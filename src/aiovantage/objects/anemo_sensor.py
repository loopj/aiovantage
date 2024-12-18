"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import AnemoSensorInterface, SensorInterface

from .sensor import Sensor
from .types import Parent


@dataclass
class AnemoSensor(Sensor, AnemoSensorInterface, SensorInterface):
    """AnemoSensor (wind sensor) object."""

    parent: Parent
