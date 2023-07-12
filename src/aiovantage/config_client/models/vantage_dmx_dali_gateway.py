"""DMX/DALI Gateway station."""

from dataclasses import dataclass

from .station_object import StationObject


@dataclass
class VantageDmxDaliGateway(StationObject):
    """DMX/DALI Gateway station."""

    class Meta:
        name = "Vantage.DmxDaliGateway"
