"""Vantage HVAC Interfacepoint zone."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface

from . import ChildDevice


@dataclass(kw_only=True)
class VantageHVACIUZoneChild(ChildDevice, ThermostatInterface):
    """Vantage HVAC Interfacepoint zone."""

    class Meta:
        name = "Vantage.HVAC-IU-Zone_CHILD"
