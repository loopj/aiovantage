"""DryContact object."""

from dataclasses import dataclass, field

from .location_object import LocationObject
from .types import Parent


@dataclass
class DryContact(LocationObject):
    """DryContact object."""

    parent: Parent

    # State
    triggered: bool | None = field(default=None, metadata={"type": "Ignore"})
