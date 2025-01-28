"""Controller holding and managing thermostats."""

from contextlib import suppress
from typing import Any

from typing_extensions import override

from aiovantage.errors import CommandError
from aiovantage.objects import Temperature, Thermostat
from aiovantage.query import QuerySet

from .base import BaseController


class ThermostatsController(BaseController[Thermostat]):
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
    async def fetch_object_state(self, obj: Thermostat) -> None:
        """Fetch the state properties of a thermostat."""
        state: dict[str, Any] = {
            "operation_mode": await obj.get_operation_mode(),
            "fan_mode": await obj.get_fan_mode(),
            "day_mode": await obj.get_day_mode(),
        }

        # Hold mode is not supported by every thermostat type.
        with suppress(CommandError):
            state["hold_mode"] = await obj.get_hold_mode()

        # Status is not available on 2.x firmware.
        with suppress(CommandError):
            state["status"] = await obj.get_status()

        self.update_state(obj, state)

    @override
    def handle_status(self, obj: Thermostat, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        state: dict[str, Any] = {}

        if status == "THERMOP":
            # STATUS THERMOP
            # -> S:THERMOP <id> <operation_mode (OFF/COOL/HEAT/AUTO)>
            match args[0]:
                case "OFF":
                    state["operation_mode"] = Thermostat.OperationMode.Off
                case "COOL":
                    state["operation_mode"] = Thermostat.OperationMode.Cool
                case "HEAT":
                    state["operation_mode"] = Thermostat.OperationMode.Heat
                case "AUTO":
                    state["operation_mode"] = Thermostat.OperationMode.Auto
                case _:
                    state["operation_mode"] = Thermostat.OperationMode.Unknown
        elif status == "THERMFAN":
            # STATUS THERMFAN
            # -> S:THERMFAN <id> <fan_mode (ON/AUTO)>
            match args[0]:
                case "ON":
                    state["fan_mode"] = Thermostat.FanMode.On
                case "AUTO":
                    state["fan_mode"] = Thermostat.FanMode.Off
                case _:
                    state["fan_mode"] = Thermostat.FanMode.Unknown
        elif status == "THERMDAY":
            # STATUS THERMDAY
            # -> S:THERMDAY <id> <day_mode (DAY/NIGHT)>
            match args[0]:
                case "DAY":
                    state["day_mode"] = Thermostat.DayMode.Day
                case "NIGHT":
                    state["day_mode"] = Thermostat.DayMode.Night
                case _:
                    state["day_mode"] = Thermostat.DayMode.Unknown
        else:
            return

        self.update_state(obj, state)

    @override
    def handle_interface_status(
        self, obj: Thermostat, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        state: dict[str, Any] = {}
        if method == "Thermostat.GetHoldMode":
            state["hold_mode"] = obj.parse_object_status(method, result, *args)
        elif method == "Thermostat.GetStatus":
            state["status"] = obj.parse_object_status(method, result, *args)

        self.update_state(obj, state)

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
