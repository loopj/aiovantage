"""Controller holding and managing Vantage modules."""

from aiovantage.command_client.interfaces import ThermostatInterface
from aiovantage.models import Thermostat

from .base import BaseController


class ThermostatsController(BaseController[Thermostat], ThermostatInterface):
    """Controller holding and managing thermostats."""

    vantage_types = ("Thermostat",)
    """The Vantage object types that this controller will fetch."""
