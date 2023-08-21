"""Blind object."""

from attr import define, field

from .blind_base import BlindBase
from .location_object import LocationObject
from .types import Parent


@define
class Blind(BlindBase, LocationObject):
    """Blind object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
