"""Blind object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.location_object import LocationObject
from aiovantage.objects.types import Parent


@dataclass
class Blind(LocationObject, BlindInterface):
    """Blind object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
