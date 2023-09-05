"""Controller holding and managing thermostats."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import ThermostatInterface
from aiovantage.models import Temperature, Thermostat
from aiovantage.query import QuerySet

from .base import BaseController, State


class ThermostatsController(BaseController[Thermostat], ThermostatInterface):
    """Controller holding and managing thermostats."""

    vantage_types = ("Thermostat",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("THERMFAN", "THERMOP", "THERMDAY")
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a thermostat."""
        return {
            "day_mode": await ThermostatInterface.get_day_mode(self, vid),
            "fan_mode": await ThermostatInterface.get_fan_mode(self, vid),
            "operation_mode": await ThermostatInterface.get_operation_mode(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a thermostat."""
        if status == "THERMFAN":
            # STATUS THERMFAN
            # -> S:THERMFAN <id> <fan_mode (ON/AUTO)>
            if args[0] == "ON":
                fan_mode = Thermostat.FanMode.ON
            elif args[0] == "AUTO":
                fan_mode = Thermostat.FanMode.OFF

            return {
                "fan_mode": fan_mode,
            }

        if status == "THERMOP":
            # STATUS THERMOP
            # -> S:THERMOP <id> <operation_mode (OFF/COOL/HEAT/AUTO)>
            if args[0] == "OFF":
                op_mode = Thermostat.OperationMode.OFF
            elif args[0] == "COOL":
                op_mode = Thermostat.OperationMode.COOL
            elif args[0] == "HEAT":
                op_mode = Thermostat.OperationMode.HEAT
            elif args[0] == "AUTO":
                op_mode = Thermostat.OperationMode.AUTO

            return {
                "operation_mode": op_mode,
            }

        if status == "THERMDAY":
            # STATUS THERMDAY
            # -> S:THERMDAY <id> <day_mode (DAY/NIGHT)>
            if args[0] == "DAY":
                day_mode = Thermostat.DayMode.DAY
            elif args[0] == "NIGHT":
                day_mode = Thermostat.DayMode.NIGHT

            return {
                "day_mode": day_mode,
            }

        return None

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
        return self.sensors(vid).filter(
            lambda obj: obj.setpoint == Temperature.Setpoint.COOL
            or obj.parent.position == 3
        )

    def heat_setpoint(self, vid: int) -> QuerySet[Temperature]:
        """Return a queryset to fetch the heat setpoint sensor for this thermostat."""
        return self.sensors(vid).filter(
            lambda obj: obj.setpoint == Temperature.Setpoint.HEAT
            or obj.parent.position == 4
        )
