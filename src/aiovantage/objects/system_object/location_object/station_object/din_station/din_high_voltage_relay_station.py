"""DIN High Voltage Relay Station."""

from dataclasses import dataclass

from . import DINStation


@dataclass(kw_only=True)
class DINHighVoltageRelayStation(DINStation):
    """DIN High Voltage Relay Station."""
