"""Base class for Vantage port device (drive-provided) objects."""

from dataclasses import dataclass

from .location_object import LocationObject


@dataclass(kw_only=True)
class PortDevice(LocationObject):
    """Base class for Vantage port device (drive-provided) objects."""

    # NOTE: Inherits from LocationObject on 2.x firmware, ParentDevice on 3.x firmware.
