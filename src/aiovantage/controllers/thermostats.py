"""Controller holding and managing thermostats."""

from contextlib import suppress
from typing import Any

from typing_extensions import override

from aiovantage.errors import CommandError
from aiovantage.object_interfaces import ThermostatInterface
from aiovantage.objects import Temperature, Thermostat
from aiovantage.query import QuerySet

from .base import BaseController


def parse_thermop(value: str) -> ThermostatInterface.OperationMode:
    """Parse a THERMOP status messages."""
    match value:
        case "OFF":
            return ThermostatInterface.OperationMode.Off
        case "COOL":
            return ThermostatInterface.OperationMode.Cool
        case "HEAT":
            return ThermostatInterface.OperationMode.Heat
        case "AUTO":
            return ThermostatInterface.OperationMode.Auto
        case _:
            return ThermostatInterface.OperationMode.Unknown


def parse_thermfan(value: str) -> ThermostatInterface.FanMode:
    """Parse a THERMFAN status messages."""
    match value:
        case "AUTO":
            return ThermostatInterface.FanMode.Off
        case "ON":
            return ThermostatInterface.FanMode.On
        case _:
            return ThermostatInterface.FanMode.Unknown


def parse_thermday(value: str) -> ThermostatInterface.DayMode:
    """Parse a THERMDAY status messages."""
    match value:
        case "DAY":
            return ThermostatInterface.DayMode.Day
        case "NIGHT":
            return ThermostatInterface.DayMode.Night
        case _:
            return ThermostatInterface.DayMode.Unknown


class ThermostatsController(BaseController[Thermostat]):
    """Controller holding and managing thermostats.

    Thermostats have a number of temperature sensors associated with them which
    represent the current indoor temperature, outdoor temperature, and the
    current cool and heat setpoints.
    """

    vantage_types = (Thermostat,)
    status_types = ("THERMFAN", "THERMOP", "THERMDAY")

    @override
    async def fetch_object_state(self, obj: Thermostat) -> None:
        """Fetch the state properties of a thermostat."""
        state: dict[str, Any] = {}
        state["operation_mode"] = await obj.get_operation_mode()
        state["fan_mode"] = await obj.get_fan_mode()
        state["day_mode"] = await obj.get_day_mode()

        # Hold mode is not supported by every thermostat type.
        with suppress(CommandError):
            state["hold_mode"] = await obj.get_hold_mode()

        # Status is not available on 2.x firmware.
        with suppress(CommandError):
            state["status"] = await obj.get_status()

        self.update_state(obj.id, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        state: dict[str, Any] = {}

        if status == "THERMOP":
            # STATUS THERMOP
            # -> S:THERMOP <id> <operation_mode (OFF/COOL/HEAT/AUTO)>
            state["operation_mode"] = parse_thermop(args[0])
        elif status == "THERMFAN":
            # STATUS THERMFAN
            # -> S:THERMFAN <id> <fan_mode (ON/AUTO)>
            state["fan_mode"] = parse_thermfan(args[0])
        elif status == "THERMDAY":
            # STATUS THERMDAY
            # -> S:THERMDAY <id> <day_mode (DAY/NIGHT)>
            state["day_mode"] = parse_thermday(args[0])
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
            state["hold_mode"] = ThermostatInterface.parse_response(
                method, result, *args
            )
        elif method == "Thermostat.GetStatus":
            state["status"] = ThermostatInterface.parse_response(method, result, *args)

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
