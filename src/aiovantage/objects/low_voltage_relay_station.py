"""Low Voltage Relay Station."""

from dataclasses import dataclass

from aiovantage.objects.station_object import StationObject


@dataclass
class LowVoltageRelayStation(StationObject):
    """Low Voltage Relay Station."""
