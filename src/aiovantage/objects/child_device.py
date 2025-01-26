"""Base class for child device objects."""

from dataclasses import dataclass

from .custom_device import CustomDevice
from .types import Parent


@dataclass(kw_only=True)
class ChildDevice(CustomDevice):
    """Base class for child device objects."""

    parent: Parent
