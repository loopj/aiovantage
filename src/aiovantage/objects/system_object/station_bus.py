"""Station bus object."""

from dataclasses import dataclass, field

from aiovantage.objects.types import Parent

from . import SystemObject


@dataclass
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
