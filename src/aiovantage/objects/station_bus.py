"""Station bus object."""

from dataclasses import dataclass, field

from aiovantage.objects.system_object import SystemObject
from aiovantage.objects.types import Parent


@dataclass
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
