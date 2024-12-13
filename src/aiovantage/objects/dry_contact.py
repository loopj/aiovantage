"""DryContact object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.button import ButtonInterface
from aiovantage.objects.location_object import LocationObject
from aiovantage.objects.types import Parent


@dataclass
class DryContact(LocationObject, ButtonInterface):
    """DryContact object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
