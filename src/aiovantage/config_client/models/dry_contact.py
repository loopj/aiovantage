"""DryContact object."""

from typing import Optional

from attr import define, field

from .child_object import ChildObject
from .location_object import LocationObject


@define
class DryContact(ChildObject, LocationObject):
    """DryContact object."""

    triggered: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
