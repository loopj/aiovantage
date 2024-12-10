"""Blind object."""

from dataclasses import dataclass, field

from aiovantage.models.location_object import LocationObject
from aiovantage.models.types import Parent
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class Blind(LocationObject, BlindInterface):
    """Blind object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
