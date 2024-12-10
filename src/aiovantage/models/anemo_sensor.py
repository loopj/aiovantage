"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass, field

from aiovantage.models.sensor import Sensor
from aiovantage.models.types import Parent
from aiovantage.object_interfaces.anemo_sensor import AnemoSensorInterface
from aiovantage.object_interfaces.sensor import SensorInterface


@dataclass
class AnemoSensor(Sensor, SensorInterface, AnemoSensorInterface):
    """AnemoSensor (wind sensor) object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
