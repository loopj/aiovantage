"""DMX Gateway."""

from dataclasses import dataclass

from .port_device import PortDevice


@dataclass
class VantageDmxGateway(PortDevice):
    """DMX Gateway."""

    class Meta:
        name = "Vantage.DmxGateway"
