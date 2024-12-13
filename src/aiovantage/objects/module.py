"""Module object."""

from dataclasses import dataclass, field

from aiovantage.objects.system_object import SystemObject
from aiovantage.objects.types import Parent


@dataclass
class Module(SystemObject):
    """Module object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
