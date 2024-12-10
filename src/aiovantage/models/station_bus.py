"""Station bus object."""

from dataclasses import dataclass, field

from aiovantage.models.system_object import SystemObject
from aiovantage.models.types import Parent


@dataclass
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
