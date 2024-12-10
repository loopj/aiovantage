"""DryContact object."""

from dataclasses import dataclass, field

from aiovantage.models.location_object import LocationObject
from aiovantage.models.types import Parent
from aiovantage.object_interfaces.button import ButtonInterface


@dataclass
class DryContact(LocationObject, ButtonInterface):
    """DryContact object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
