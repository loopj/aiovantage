"""Blind object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class Blind(BlindBase, LocationObject):
    """Blind object."""

    @dataclass
    class Movement:
        open: float = 5.0
        close: float = 5.0

    parent: Parent
    movement: Movement | None = None
