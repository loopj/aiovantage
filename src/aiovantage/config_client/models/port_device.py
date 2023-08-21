"""Base class for Vantage port devices."""


from attr import define

from .parent_device import ParentDevice


@define
class PortDevice(ParentDevice):
    """Base class for Vantage port devices."""
