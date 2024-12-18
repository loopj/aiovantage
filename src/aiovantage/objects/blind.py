"""Blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .location_object import LocationObject
from .types import Parent


@dataclass
class Blind(LocationObject, BlindInterface):
    """Blind object."""

    parent: Parent