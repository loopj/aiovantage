"""Station bus object."""

from dataclasses import dataclass, field

from .system_object import SystemObject
from .types import Parent


@dataclass
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
