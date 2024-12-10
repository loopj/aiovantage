"""Base class for parent device objects."""

from dataclasses import dataclass

from aiovantage.models.custom_device import CustomDevice


@dataclass
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""
