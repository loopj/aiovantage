from decimal import Decimal
from typing import Any, Dict, Sequence, Union

from typing_extensions import override

from aiovantage.config_client.objects import OmniSensor
from aiovantage.controllers.base import StatefulController


class OmniSensorsController(StatefulController[OmniSensor]):
    # Fetch the following object types from Vantage
    vantage_types = ("OmniSensor",)

    # Subscribe to status updates from the event log
    event_log_status = True

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of an OmniSensor.

        state: Dict[str, Any] = {}
        state["level"] = await self.get_level(id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, method: str, args: Sequence[str]) -> None:
        # Handle state changes for an OmniSensor.

        omni_sensor: OmniSensor = self[id]
        if method != omni_sensor.get.method:
            return

        state: Dict[str, Any] = {}
        state["level"] = self.parse_get_level_status(omni_sensor, args)

        self.update_state(id, state)

    async def get_level(self, id: int) -> Union[int, Decimal]:
        """
        Get the level of an OmniSensor.

        Args:
            id: The ID of the sensor.

        Returns:
            The level of the sensor.
        """

        omni_sensor: OmniSensor = self[id]

        # INVOKE <id> <method>
        # -> R:INVOKE <id> <value> <method>
        response = await self.command_client.command(
            "INVOKE", id, omni_sensor.get.method
        )

        # Convert the level to the correct type
        if omni_sensor.get.formula.return_type == "fixed":
            level = Decimal(response.args[1])
            if omni_sensor.get.formula.level_type == "fixed":
                return level
            else:
                return int(level)
        else:
            level = Decimal(response.args[1]) / 1000
            if omni_sensor.get.formula.level_type == "fixed":
                return level
            else:
                return int(level)

    @classmethod
    def parse_get_level_status(
        cls, omni_sensor: OmniSensor, args: Sequence[str]
    ) -> Union[int, Decimal]:
        # Parse an OmniSensor "GetLevel" event, eg. "PowerSensor.GetPower"

        # ELLOG STATUS ON
        # -> EL: <id> <method> <value>
        # STATUS ADD <id>
        # -> S:STATUS <id> <method> <value>
        level = Decimal(args[0]) / 1000
        if omni_sensor.get.formula.level_type == "fixed":
            return level
        else:
            return int(level)
