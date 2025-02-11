from aiovantage.objects import Thermostat

from .base import BaseController


class ThermostatsController(BaseController[Thermostat]):
    """Thermostats controller.

    Thermostats have a number of temperature sensors associated with them which
    represent the current indoor temperature, outdoor temperature, and the
    current cool and heat setpoints.
    """

    vantage_types = ("Thermostat",)
