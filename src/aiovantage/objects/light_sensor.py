"""Light sensor object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.light_sensor import LightSensorInterface
from aiovantage.object_interfaces.sensor import SensorInterface
from aiovantage.objects.sensor import Sensor
from aiovantage.objects.types import Parent


@dataclass
class LightSensor(Sensor, SensorInterface, LightSensorInterface):
    """Light sensor object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
