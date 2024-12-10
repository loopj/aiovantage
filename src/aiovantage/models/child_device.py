"""Base class for child device objects."""

from dataclasses import dataclass, field

from aiovantage.models.custom_device import CustomDevice
from aiovantage.models.types import Parent


@dataclass
class ChildDevice(CustomDevice):
    """Base class for child device objects."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
