"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass

from .sensor import Sensor


@dataclass
class AnemoSensor(Sensor):
    """AnemoSensor (wind sensor) object."""
