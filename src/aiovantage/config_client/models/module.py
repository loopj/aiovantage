"""Module object."""

from dataclasses import dataclass

from .child_object import ChildObject
from .system_object import SystemObject


@dataclass
class Module(ChildObject, SystemObject):
    """Module object."""
