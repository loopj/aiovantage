"""DryContact object."""

from typing import Optional

from attr import define, field

from .location_object import LocationObject
from .types import Parent


@define
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
