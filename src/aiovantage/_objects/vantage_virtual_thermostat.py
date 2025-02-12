"""Vantage Virtual Thermostat objects."""

from dataclasses import dataclass

from aiovantage.object_interfaces import FanInterface, ThermostatInterface

from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageVirtualThermostatPort(PortDevice, ThermostatInterface, FanInterface):
    """Vantage Virtual Thermostat."""

    class Meta:
        name = "Vantage.VirtualThermostat_PORT"
