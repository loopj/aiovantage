"""Vantage Generic HVAC RS485."""

from dataclasses import dataclass

from . import PortDevice


@dataclass(kw_only=True)
class VantageGenericHVACRS485Port(PortDevice):
    """Vantage Generic HVAC RS485."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_PORT"
