"""Sensor object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from .location_object import LocationObject


@dataclass
class Sensor(LocationObject):
    """Sensor object."""

    def __post_init__(self) -> None:
        """Post init."""
        self.level: Union[int, Decimal, None] = None
