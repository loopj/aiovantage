"""DMX Gateway."""

from dataclasses import dataclass

from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageDmxGateway(PortDevice):
    """DMX Gateway."""

    class Meta:
        name = "Vantage.DmxGateway"
