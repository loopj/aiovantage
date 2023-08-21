"""DMX Gateway."""

from attr import define

from .port_device import PortDevice


@define
class VantageDmxGateway(PortDevice):
    """DMX Gateway."""

    class Meta:
        name = "Vantage.DmxGateway"
