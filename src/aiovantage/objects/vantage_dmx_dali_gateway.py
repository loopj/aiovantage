"""DMX/DALI Gateway station."""

from dataclasses import dataclass, field

from .din_station import DINStation


@dataclass(kw_only=True)
class VantageDmxDaliGateway(DINStation):
    """DMX/DALI Gateway station."""

    class Meta:
        name = "Vantage.DmxDaliGateway"

    ip_address: str = field(metadata={"name": "IPAddress"})
    mode: str
