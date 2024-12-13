"""Keypad Station."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import SounderInterface
from aiovantage.objects.types import Parent

from .. import StationObject


@dataclass
class Keypad(StationObject, SounderInterface):
    """Keypad Station."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
