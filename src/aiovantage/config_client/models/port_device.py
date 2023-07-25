"""Base class for Vantage port devices."""


from dataclasses import dataclass

from .system_object import SystemObject


@dataclass
class PortDevice(SystemObject):
    """Base class for Vantage port devices."""
