"""Vantage Generic HVAC RS485 zone (without fan speed)."""

from dataclasses import dataclass

from aiovantage.object_interfaces.thermostat import ThermostatInterface

from . import ChildDevice


@dataclass(kw_only=True)
class VantageGenericHVACRS485ZoneWithoutFanSpeedChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 zone (without fan speed)."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Zone_without_FanSpeed_CHILD"
