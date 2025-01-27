"""DryContact object."""

from dataclasses import dataclass, field

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class DryContact(LocationObject):
    """DryContact object."""

    parent: Parent
    down: int = 0
    up: int = 0
    reverse_polarity: bool
    hold_on_time: float = 0

    # State
    triggered: bool | None = field(default=None, metadata={"type": "Ignore"})
