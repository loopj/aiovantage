"""Blind object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .location_object import LocationObject
from .types import Parent


@dataclass
class Blind(BlindBase, LocationObject):
    """Blind object."""

    parent: Parent
