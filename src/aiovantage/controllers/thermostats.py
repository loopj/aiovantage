"""Controller holding and managing thermostats."""

from aiovantage.command_client.object_interfaces import ThermostatInterface
from aiovantage.models import Thermostat

from .base import BaseController


class ThermostatsController(BaseController[Thermostat], ThermostatInterface):
    """Controller holding and managing thermostats."""

    vantage_types = ("Thermostat",)
    """The Vantage object types that this controller will fetch."""
