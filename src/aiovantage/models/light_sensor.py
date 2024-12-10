"""Light sensor object."""

from dataclasses import dataclass, field

from aiovantage.models.sensor import Sensor
from aiovantage.models.types import Parent
from aiovantage.object_interfaces.light_sensor import LightSensorInterface
from aiovantage.object_interfaces.sensor import SensorInterface


@dataclass
class LightSensor(Sensor, SensorInterface, LightSensorInterface):
    """Light sensor object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
