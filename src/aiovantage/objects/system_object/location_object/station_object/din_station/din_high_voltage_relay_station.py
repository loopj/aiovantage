"""DIN High Voltage Relay Station."""

from dataclasses import dataclass

from . import DINStation


@dataclass
class DINHighVoltageRelayStation(DINStation):
    """DIN High Voltage Relay Station."""
