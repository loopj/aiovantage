"""Base class for child device objects."""

from dataclasses import dataclass

from .child_object import ChildObject
from .custom_device import CustomDevice


@dataclass
class ChildDevice(ChildObject, CustomDevice):
    """Base class for child device objects."""
