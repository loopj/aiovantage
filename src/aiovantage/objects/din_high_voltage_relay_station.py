"""DIN High Voltage Relay Station."""

from dataclasses import dataclass

from .din_station import DINStation


@dataclass
class DINHighVoltageRelayStation(DINStation):
    """DIN High Voltage Relay Station."""
