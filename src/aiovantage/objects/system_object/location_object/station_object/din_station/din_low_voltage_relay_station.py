"""DIN Low Voltage Relay Station."""

from dataclasses import dataclass

from . import DINStation


@dataclass
class DINLowVoltageRelayStation(DINStation):
    """DIN Low Voltage Relay Station."""
