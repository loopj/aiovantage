"""Base class for Vantage port device (drive-provided) objects."""

from dataclasses import dataclass

from .parent_device import ParentDevice


@dataclass(kw_only=True)
class PortDevice(ParentDevice):
    """Base class for Vantage port device (driver-provided) objects."""
