"""Vantage Virtual Thermostat objects."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ThermostatInterface

from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageVirtualThermostatPort(PortDevice, ThermostatInterface):
    """Vantage Virtual Thermostat."""

    class Meta:
        name = "Vantage.VirtualThermostat_PORT"
