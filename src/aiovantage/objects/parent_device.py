"""Base class for parent device objects."""

from dataclasses import dataclass

from aiovantage.objects.custom_device import CustomDevice


@dataclass
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""
