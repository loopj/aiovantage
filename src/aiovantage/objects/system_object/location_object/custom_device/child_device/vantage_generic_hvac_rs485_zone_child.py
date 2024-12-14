"""Vantage Generic HVAC RS485 zone."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface

from . import ChildDevice


@dataclass(kw_only=True)
class VantageGenericHVACRS485ZoneChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 zone."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Zone_CHILD"
