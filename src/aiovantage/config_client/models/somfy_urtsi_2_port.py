"""Somfy URTSI 2 port device."""

from dataclasses import dataclass

from .port_device import PortDevice


@dataclass
class SomfyURTSI2Port(PortDevice):
    """Somfy URTSI 2 port device."""

    class Meta:
        name = "Somfy.URTSI_2_PORT"
