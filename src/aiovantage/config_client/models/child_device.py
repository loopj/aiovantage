"""Base class for child device objects."""

from attr import define

from .child_object import ChildObject
from .custom_device import CustomDevice


@define
class ChildDevice(ChildObject, CustomDevice):
    """Base class for child device objects."""
