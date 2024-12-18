"""Controller holding and managing thermostats."""

from contextlib import suppress
from typing import Any

from typing_extensions import override

from aiovantage.errors import CommandError
from aiovantage.models import Temperature, Thermostat
from aiovantage.object_interfaces import ThermostatInterface
from aiovantage.query import QuerySet

from .base import BaseController


class ThermostatsController(BaseController[Thermostat], ThermostatInterface):
    """Controller holding and managing thermostats.

    Thermostats have a number of temperature sensors associated with them which
    represent the current indoor temperature, outdoor temperature, and the
    current cool and heat setpoints.
    """

    vantage_types = ("Thermostat",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("THERMFAN", "THERMOP", "THERMDAY")
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a thermostat."""
        state = {
            "operation_mode": await ThermostatInterface.get_operation_mode(self, vid),
            "fan_mode": await ThermostatInterface.get_fan_mode(self, vid),
            "day_mode": await ThermostatInterface.get_day_mode(self, vid),
        }

        # Hold mode is not supported by every thermostat type.
        with suppress(CommandError):
            state["hold_mode"] = await ThermostatInterface.get_hold_mode(self, vid)

        # Status is not available on 2.x firmware.
        with suppress(CommandError):
            state["status"] = await ThermostatInterface.get_status(self, vid)

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        state: dict[str, Any] = {}

        if status == "THERMOP":
            # STATUS THERMOP
            # -> S:THERMOP <id> <operation_mode (OFF/COOL/HEAT/AUTO)>
            state["operation_mode"] = Thermostat.OperationMode[args[0]]
        elif status == "THERMFAN":
            # STATUS THERMFAN
            # -> S:THERMFAN <id> <fan_mode (ON/AUTO)>
            state["fan_mode"] = Thermostat.FanMode[args[0]]
        elif status == "THERMDAY":
            # STATUS THERMDAY
            # -> S:THERMDAY <id> <day_mode (DAY/NIGHT)>
            state["day_mode"] = Thermostat.DayMode[args[0]]
        else:
            return

        self.update_state(vid, state)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        state: dict[str, Any] = {}
        if method == "Thermostat.GetHoldMode":
            state["hold_mode"] = self.parse_response(method, result, *args)
        elif method == "Thermostat.GetStatus":
            state["status"] = self.parse_response(method, result, *args)

        self.update_state(vid, state)

    def sensors(self, vid: int) -> QuerySet[Temperature]:
        """Return all sensors associated with this thermostat."""
        return self._vantage.temperature_sensors.filter(
            lambda obj: obj.parent.id == vid
        )

    def indoor_sensor(self, vid: int) -> QuerySet[Temperature]:
        """Return a queryset to fetch the indoor temperature sensor for this thermostat."""
        return self.sensors(vid).filter(lambda obj: obj.parent.position == 1)

    def outdoor_sensor(self, vid: int) -> QuerySet[Temperature]:
        """Return a queryset to fetch the outdoor temperature sensor for this thermostat."""
        return self.sensors(vid).filter(lambda obj: obj.parent.position == 2)

    def cool_setpoint(self, vid: int) -> QuerySet[Temperature]:
        """Return a queryset to fetch the cool setpoint sensor for this thermostat."""
        return self.sensors(vid).filter(lambda obj: obj.parent.position == 3)

    def heat_setpoint(self, vid: int) -> QuerySet[Temperature]:
        """Return a queryset to fetch the heat setpoint sensor for this thermostat."""
        return self.sensors(vid).filter(lambda obj: obj.parent.position == 4)
