"""Light sensor object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.light_sensor import LightSensorInterface
from aiovantage.object_interfaces.sensor import SensorInterface
from aiovantage.objects.types import Parent

from . import Sensor


@dataclass(kw_only=True)
class LightSensor(Sensor, SensorInterface, LightSensorInterface):
    """Light sensor object."""

    parent: Parent
