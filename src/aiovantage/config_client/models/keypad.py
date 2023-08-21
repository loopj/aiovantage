"""Keypad Station."""

from attr import define, field

from .station_object import StationObject
from .types import Parent


@define
class Keypad(StationObject):
    """Keypad Station."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
