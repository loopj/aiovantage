"""Base class for Vantage port devices."""


from attr import define

from .location_object import LocationObject

# NOTE: Inherits from LocationObject on 2.x firmware, ParentDevice on 3.x firmware.


@define
class PortDevice(LocationObject):
    """Base class for Vantage port devices."""
