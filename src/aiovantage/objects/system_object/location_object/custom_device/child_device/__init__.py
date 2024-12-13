"""Base class for child device objects."""

from dataclasses import dataclass, field

from aiovantage.objects.types import Parent

from .. import CustomDevice


@dataclass
class ChildDevice(CustomDevice):
    """Base class for child device objects."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
