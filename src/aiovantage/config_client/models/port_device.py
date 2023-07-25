"""Base class for Vantage port devices."""


from dataclasses import dataclass

from .parent_device import ParentDevice


@dataclass
class PortDevice(ParentDevice):
    """Base class for Vantage port devices."""
