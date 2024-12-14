"""Vantage Generic HVAC RS485 compound."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface

from . import ChildDevice


@dataclass(kw_only=True)
class VantageGenericHVACRS485CompoundChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 compound."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Compound_CHILD"
