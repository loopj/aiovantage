"""Controller holding and managing Vantage omni sensors."""

from decimal import Decimal
from typing import Any, Dict, Sequence, Union

from typing_extensions import override

from aiovantage.config_client.objects import OmniSensor
from aiovantage.controllers.base import StatefulController


class OmniSensorsController(StatefulController[OmniSensor]):
    """Controller holding and managing Vantage omni sensors."""

    # Fetch the following object types from Vantage
    vantage_types = ("OmniSensor",)

    # Subscribe to status updates from the Enhanced Log
    enhanced_log_status = True

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of an omni sensor."""

        state: Dict[str, Any] = {
            "level": await self.get_level(vid),
        }

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for an omni sensor."""

        omni_sensor: OmniSensor = self[vid]
        if status != omni_sensor.get.method:
            return

        state: Dict[str, Any] = {
            "level": self.parse_get_level_status(omni_sensor, args),
        }

        self.update_state(vid, state)

    async def get_level(self, vid: int, cached: bool = False) -> Union[int, Decimal]:
        """Get the level of an OmniSensor.

        Args:
            vid: The ID of the sensor.
            cached: Whether to use the cached value or fetch a new one.

        Returns:
            The level of the sensor.
        """

        omni_sensor: OmniSensor = self[vid]

        # Figure out which get method to use, hardware or software (cached)
        method = omni_sensor.get.method if cached else omni_sensor.get.method_hw

        # INVOKE <id> <method>
        # -> R:INVOKE <id> <value> <method>
        response = await self.command_client.command("INVOKE", vid, method)

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
        """Parse an OmniSensor 'GetLevel' event, eg. 'PowerSensor.GetPower'."""

        # ELLOG STATUS ON
        # -> EL: <id> <method> <value>
        # STATUS ADD <id>
        # -> S:STATUS <id> <method> <value>
        level = Decimal(args[0]) / 1000
        if omni_sensor.get.formula.level_type == "fixed":
            return level
        else:
            return int(level)
