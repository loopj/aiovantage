"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.anemo_sensor import AnemoSensorInterface
from aiovantage.object_interfaces.sensor import SensorInterface
from aiovantage.objects.types import Parent

from . import Sensor


@dataclass
class AnemoSensor(Sensor, SensorInterface, AnemoSensorInterface):
    """AnemoSensor (wind sensor) object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )