"""Blind object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .child_object import ChildObject
from .location_object import LocationObject


@dataclass
class Blind(BlindBase, LocationObject, ChildObject):
    """Blind object."""
