"""DMX/DALI Gateway station."""

from attr import define

from .station_object import StationObject


@define
class VantageDmxDaliGateway(StationObject):
    """DMX/DALI Gateway station."""

    class Meta:
        name = "Vantage.DmxDaliGateway"
