"""DIN High Voltage Relay Station."""

from dataclasses import dataclass

from .din_station import DINStation


@dataclass(kw_only=True)
class DINHighVoltageRelayStation(DINStation):
    """DIN High Voltage Relay Station."""
