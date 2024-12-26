"""Vantage HVAC-IU objects."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ThermostatInterface

from .child_device import ChildDevice
from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageHVACIUPort(PortDevice):
    """Vantage HVAC-IU port device."""

    class Meta:
        name = "Vantage.HVAC-IU_PORT"


@dataclass(kw_only=True)
class VantageHVACIULineChild(ChildDevice):
    """Vantage HVAC-IU line child device."""

    class Meta:
        name = "Vantage.HVAC-IU-Line_CHILD"


@dataclass(kw_only=True)
class VantageHVACIUZoneChild(ChildDevice, ThermostatInterface):
    """Vantage HVAC-IU zone child device."""

    class Meta:
        name = "Vantage.HVAC-IU-Zone_CHILD"
