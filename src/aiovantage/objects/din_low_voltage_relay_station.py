"""DIN Low Voltage Relay Station."""

from dataclasses import dataclass

from aiovantage.objects.din_station import DINStation


@dataclass
class DINLowVoltageRelayStation(DINStation):
    """DIN Low Voltage Relay Station."""
