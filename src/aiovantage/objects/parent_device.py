"""Base class for parent device objects."""

from dataclasses import dataclass

from .custom_device import CustomDevice


@dataclass(kw_only=True)
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""
