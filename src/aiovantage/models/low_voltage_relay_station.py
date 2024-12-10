"""Low Voltage Relay Station."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject


@dataclass
class LowVoltageRelayStation(StationObject):
    """Low Voltage Relay Station."""
