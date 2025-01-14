"""Controller holding and managing thermostats."""

from aiovantage.objects import Thermostat

from .base import BaseController

# The various "thermostat" object types don't all inherit from the same base class,
# so for typing purposes we'll use a union of all the types.
ThermostatTypes = Thermostat


class ThermostatsController(BaseController[ThermostatTypes]):
    """Controller holding and managing thermostats."""

    vantage_types = (Thermostat,)
