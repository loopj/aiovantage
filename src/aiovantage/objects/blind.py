"""Blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class Blind(LocationObject, BlindInterface):
    """Blind object."""

    @dataclass
    class Movement:
        open: float = 5.0
        close: float = 5.0

    parent: Parent
    movement: Movement | None = None
