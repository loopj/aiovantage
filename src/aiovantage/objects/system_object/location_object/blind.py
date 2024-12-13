"""Blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.types import Parent

from . import LocationObject


@dataclass(kw_only=True)
class Blind(LocationObject, BlindInterface):
    """Blind object."""

    parent: Parent
