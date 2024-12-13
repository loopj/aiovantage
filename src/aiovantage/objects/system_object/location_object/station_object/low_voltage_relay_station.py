"""Low Voltage Relay Station."""

from dataclasses import dataclass

from . import StationObject


@dataclass(kw_only=True)
class LowVoltageRelayStation(StationObject):
    """Low Voltage Relay Station."""
