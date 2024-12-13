"""Base class for Vantage port devices."""

from dataclasses import dataclass

from .. import ParentDevice


@dataclass(kw_only=True)
class PortDevice(ParentDevice):
    """Base class for Vantage port devices."""

    # NOTE: Inherits from LocationObject on 2.x firmware
