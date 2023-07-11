"""DryContact object."""

from dataclasses import dataclass, field
from typing import Optional

from .child_object import ChildObject
from .location_object import LocationObject


@dataclass
class DryContact(LocationObject, ChildObject):
    """DryContact object."""

    triggered: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
