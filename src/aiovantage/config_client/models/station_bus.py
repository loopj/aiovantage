"""Station bus object."""

from dataclasses import dataclass

from .child_object import ChildObject
from .system_object import SystemObject


@dataclass
class StationBus(ChildObject, SystemObject):
    """Station bus object."""
