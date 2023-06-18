"""Temperature object."""

from dataclasses import dataclass

from .sensor import Sensor


@dataclass
class Temperature(Sensor):
    """Temperature object."""
