"""Module object."""

from dataclasses import dataclass, field

from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass
class Module(SystemObject):
    """Module object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
