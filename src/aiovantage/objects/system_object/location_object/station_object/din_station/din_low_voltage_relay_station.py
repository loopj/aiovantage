"""DIN Low Voltage Relay Station."""

from dataclasses import dataclass

from . import DINStation


@dataclass(kw_only=True)
class DINLowVoltageRelayStation(DINStation):
    """DIN Low Voltage Relay Station."""
