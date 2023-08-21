"""Blind object."""

from attr import define

from .blind_base import BlindBase
from .child_object import ChildObject
from .location_object import LocationObject


@define
class Blind(BlindBase, ChildObject, LocationObject):
    """Blind object."""
