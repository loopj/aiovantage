"""Controller holding and managing thermostats."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import ThermostatInterface
from aiovantage.models import Thermostat

from .base import BaseController, State


class ThermostatsController(BaseController[Thermostat], ThermostatInterface):
    """Controller holding and managing thermostats."""

    vantage_types = ("Thermostat",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("THERMDAY", "THERMFAN", "THERMOP")
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a task."""
        return {
            "day_mode": await ThermostatInterface.get_day_mode(self, vid),
            "fan_mode": await ThermostatInterface.get_fan_mode(self, vid),
            "operation_mode": await ThermostatInterface.get_operation_mode(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a task."""
        if status == "THERMDAY":
            # STATUS THERMDAY
            # -> S:THERMDAY <id> <day_mode (DAY/NIGHT)>
            day_mode: Thermostat.DayMode = Thermostat.DayMode.Unknown
            if args[0] == "DAY":
                day_mode = Thermostat.DayMode.Day
            elif args[0] == "NIGHT":
                day_mode = Thermostat.DayMode.Night

            return {
                "day_mode": day_mode,
            }

        if status == "THERMFAN":
            # STATUS THERMFAN
            # -> S:THERMFAN <id> <fan_mode (ON/AUTO)>
            fan_mode: Thermostat.FanMode = Thermostat.FanMode.Unknown
            if args[0] == "ON":
                fan_mode = Thermostat.FanMode.On
            elif args[0] == "AUTO":
                fan_mode = Thermostat.FanMode.Off

            return {
                "fan_mode": fan_mode,
            }

        if status == "THERMOP":
            # STATUS THERMOP
            # -> S:THERMOP <id> <operation_mode (OFF/COOL/HEAT/AUTO)>
            op_mode: Thermostat.OperationMode = Thermostat.OperationMode.Unknown
            if args[0] == "OFF":
                op_mode = Thermostat.OperationMode.Off
            elif args[0] == "COOL":
                op_mode = Thermostat.OperationMode.Cool
            elif args[0] == "HEAT":
                op_mode = Thermostat.OperationMode.Heat
            elif args[0] == "AUTO":
                op_mode = Thermostat.OperationMode.Auto

            return {
                "operation_mode": op_mode,
            }

        return None
