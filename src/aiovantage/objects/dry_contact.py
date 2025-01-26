"""DryContact object."""

from dataclasses import dataclass, field

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class DryContact(LocationObject):
    """DryContact object."""

    parent: Parent

    # State
    triggered: bool | None = field(default=None, metadata={"type": "Ignore"})
