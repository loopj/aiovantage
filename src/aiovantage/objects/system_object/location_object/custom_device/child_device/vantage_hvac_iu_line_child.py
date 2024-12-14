"""Vantage HVAC Interfacepoint line."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface

from . import ChildDevice


@dataclass(kw_only=True)
class VantageHVACIULineChild(ChildDevice, ThermostatInterface):
    """Vantage HVAC Interfacepoint line."""

    class Meta:
        name = "Vantage.HVAC-IU-Line_CHILD"
