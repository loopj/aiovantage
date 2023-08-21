"""Station bus object."""

from attr import define

from .child_object import ChildObject
from .system_object import SystemObject


@define
class StationBus(ChildObject, SystemObject):
    """Station bus object."""
