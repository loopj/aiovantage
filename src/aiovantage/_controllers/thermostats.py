from aiovantage.objects import (
    Thermostat,
    VantageGenericHVACRS485CompoundChild,
    VantageGenericHVACRS485ZoneChild,
    VantageGenericHVACRS485ZoneWithoutFanSpeedChild,
    VantageHVACIUZoneChild,
    VantageVirtualThermostatPort,
)

from .base import BaseController

ThermostatTypes = (
    Thermostat
    | VantageGenericHVACRS485CompoundChild
    | VantageGenericHVACRS485ZoneChild
    | VantageGenericHVACRS485ZoneWithoutFanSpeedChild
    | VantageHVACIUZoneChild
    | VantageVirtualThermostatPort
)
"""Types managed by the thermostats controller."""


class ThermostatsController(BaseController[ThermostatTypes]):
    """Thermostats controller.

    Thermostats have a number of temperature objects associated with them which
    represent the current indoor temperature, outdoor temperature, and the
    current cool and heat setpoints.
    """

    vantage_types = (
        "Thermostat",
        "Vantage.Generic_HVAC_RS485_Compound_CHILD",
        "Vantage.Generic_HVAC_RS485_Zone_CHILD",
        "Vantage.Generic_HVAC_RS485_Zone_without_FanSpeed_CHILD",
        "Vantage.HVAC-IU-Zone_CHILD",
        "Vantage.VirtualThermostat_PORT",
    )
