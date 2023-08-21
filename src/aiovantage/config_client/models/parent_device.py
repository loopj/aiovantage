"""Base class for parent device objects."""

from attr import define

from .custom_device import CustomDevice


@define
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""
