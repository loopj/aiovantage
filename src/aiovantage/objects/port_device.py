"""Base class for Vantage port device (driver-provided) objects."""

from dataclasses import dataclass

from .location_object import LocationObject

# NOTE: Inherits from LocationObject on 2.x firmware, ParentDevice on 3.x firmware.


@dataclass(kw_only=True)
class PortDevice(LocationObject):
    """Base class for Vantage port device (driver-provided) objects."""
