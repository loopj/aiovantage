"""Station bus object."""

from attr import define, field

from .system_object import SystemObject
from .types import Parent


@define
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
