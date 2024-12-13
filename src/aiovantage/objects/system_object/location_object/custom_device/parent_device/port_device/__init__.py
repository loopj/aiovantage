"""Base class for Vantage port devices."""

from dataclasses import dataclass

from .. import ParentDevice

# NOTE: Inherits from LocationObject on 2.x firmware, ParentDevice on 3.x firmware.


@dataclass
class PortDevice(ParentDevice):
    """Base class for Vantage port devices."""
