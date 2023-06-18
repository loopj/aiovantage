"""Light sensor object."""

from dataclasses import dataclass

from .sensor import Sensor


@dataclass
class LightSensor(Sensor):
    """Light sensor object."""
