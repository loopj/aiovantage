from aiovantage.objects import (
    Thermostat,
    VantageGenericHVACRS485ZoneChild,
    VantageGenericHVACRS485ZoneWithoutFanSpeedChild,
    VantageHVACIUZoneChild,
    VantageVirtualThermostatPort,
)

from .base import BaseController

ThermostatTypes = (
    Thermostat
    | VantageGenericHVACRS485ZoneChild
    | VantageGenericHVACRS485ZoneWithoutFanSpeedChild
    | VantageHVACIUZoneChild
    | VantageVirtualThermostatPort
)
"""Types managed by the thermostats controller."""


class ThermostatsController(BaseController[ThermostatTypes]):
    """Thermostats controller."""

    vantage_types = (
        "Thermostat",
        "Vantage.Generic_HVAC_RS485_Zone_CHILD",
        "Vantage.Generic_HVAC_RS485_Zone_without_FanSpeed_CHILD",
        "Vantage.HVAC-IU-Zone_CHILD",
        "Vantage.VirtualThermostat_PORT",
    )
