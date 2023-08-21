"""Base class for child device objects."""

from attr import define, field

from .custom_device import CustomDevice
from .types import Parent


@define
class ChildDevice(CustomDevice):
    """Base class for child device objects."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
