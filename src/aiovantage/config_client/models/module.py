"""Module object."""

from attr import define

from .child_object import ChildObject
from .system_object import SystemObject


@define
class Module(ChildObject, SystemObject):
    """Module object."""
