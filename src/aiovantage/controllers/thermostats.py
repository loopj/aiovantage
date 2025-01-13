"""Controller holding and managing thermostats."""

from aiovantage.objects import Thermostat

from .base import BaseController


class ThermostatsController(BaseController[Thermostat]):
    """Controller holding and managing thermostats."""

    vantage_types = (Thermostat,)
