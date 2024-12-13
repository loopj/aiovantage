"""Keypad Station."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import SounderInterface
from aiovantage.objects.station_object import StationObject
from aiovantage.objects.types import Parent


@dataclass
class Keypad(StationObject, SounderInterface):
    """Keypad Station."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
