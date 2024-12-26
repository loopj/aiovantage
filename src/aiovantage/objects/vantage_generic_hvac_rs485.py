"""Vantage Generic HVAC RS485 objects."""

from aiovantage.object_interfaces import ThermostatInterface

from .child_device import ChildDevice
from .port_device import PortDevice


class VantageGenericHVACRS485Port(PortDevice):
    """Vantage Generic HVAC RS485 port device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_PORT"


class VantageGenericHVACRS485TechContactsChild(ChildDevice):
    """Vantage Generic HVAC RS485 tech contacts child device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_TechContacts_CHILD"


class VantageGenericHVACRS485CompoundChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 compound child device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Compound_CHILD"


class VantageGenericHVACRS485ZoneChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 zone child device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Zone_CHILD"


class VantageGenericHVACRS485ZoneWithoutFanSpeedChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 zone child device without fan speed."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Zone_without_FanSpeed_CHILD"