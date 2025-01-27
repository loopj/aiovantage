"""DMX/DALI Gateway station."""

from dataclasses import dataclass, field

from .station_object import StationObject


@dataclass(kw_only=True)
class VantageDmxDaliGateway(StationObject):
    """DMX/DALI Gateway station."""

    class Meta:
        name = "Vantage.DmxDaliGateway"

    ip_address: str = field(metadata={"name": "IPAddress"})
    mode: str
