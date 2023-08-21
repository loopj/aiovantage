"""Somfy RS-485 SDN 2.0."""
from attr import define

from .port_device import PortDevice


@define
class SomfyRS485SDN20Port(PortDevice):
    """Somfy RS-485 SDN 2.0."""

    class Meta:
        name = "Somfy.RS-485_SDN_2_x2E_0_PORT"
