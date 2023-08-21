"""Somfy URTSI 2 port device."""
from attr import define

from .port_device import PortDevice


@define
class SomfyURTSI2Port(PortDevice):
    """Somfy URTSI 2 port device."""

    class Meta:
        name = "Somfy.URTSI_2_PORT"
