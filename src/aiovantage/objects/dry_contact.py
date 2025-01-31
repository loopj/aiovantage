"""DryContact object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ButtonInterface

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class DryContact(LocationObject, ButtonInterface):
    """DryContact object."""

    parent: Parent
    down: int = 0
    up: int = 0
    reverse_polarity: bool
    hold_on_time: float = 0
