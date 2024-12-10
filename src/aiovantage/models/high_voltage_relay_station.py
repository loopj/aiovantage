"""High Voltage Relay Station."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject


@dataclass
class HighVoltageRelayStation(StationObject):
    """High Voltage Relay Station."""
