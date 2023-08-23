"""DryContact object."""

from dataclasses import dataclass, field
from typing import Optional

from .location_object import LocationObject
from .types import Parent


@dataclass
class DryContact(LocationObject):
    """DryContact object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    triggered: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
