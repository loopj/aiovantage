"""High Voltage Relay Station."""

from dataclasses import dataclass

from . import StationObject


@dataclass(kw_only=True)
class HighVoltageRelayStation(StationObject):
    """High Voltage Relay Station."""
