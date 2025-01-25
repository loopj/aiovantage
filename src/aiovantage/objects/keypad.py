"""Keypad Station."""

from dataclasses import dataclass, field

from .station_object import StationObject
from .types import Parent


@dataclass
class Keypad(StationObject):
    """Keypad Station."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
