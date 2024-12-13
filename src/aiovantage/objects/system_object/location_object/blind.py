"""Blind object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.types import Parent

from . import LocationObject


@dataclass
class Blind(LocationObject, BlindInterface):
    """Blind object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
