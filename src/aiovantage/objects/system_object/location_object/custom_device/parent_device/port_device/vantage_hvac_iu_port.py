"""Vantage HVAC Interfacepoint."""

from dataclasses import dataclass

from . import PortDevice


@dataclass(kw_only=True)
class VantageHVACIUPort(PortDevice):
    """Vantage HVAC Interfacepoint."""

    class Meta:
        name = "Vantage.HVAC-IU_PORT"
