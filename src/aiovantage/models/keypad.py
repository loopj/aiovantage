"""Keypad Station."""

from dataclasses import dataclass, field

from aiovantage.models.station_object import StationObject
from aiovantage.models.types import Parent
from aiovantage.object_interfaces import SounderInterface


@dataclass
class Keypad(StationObject, SounderInterface):
    """Keypad Station."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
