"""Vantage HVAC-IU objects."""

from aiovantage.object_interfaces import ThermostatInterface

from .child_device import ChildDevice
from .port_device import PortDevice


class VantageHVACIUPort(PortDevice):
    """Vantage HVAC-IU port device."""

    class Meta:
        name = "Vantage.HVAC-IU_PORT"


class VantageHVACIULineChild(ChildDevice):
    """Vantage HVAC-IU line child device."""

    class Meta:
        name = "Vantage.HVAC-IU-Line_CHILD"


class VantageHVACIUZoneChild(ChildDevice, ThermostatInterface):
    """Vantage HVAC-IU zone child device."""

    class Meta:
        name = "Vantage.HVAC-IU-Zone_CHILD"
