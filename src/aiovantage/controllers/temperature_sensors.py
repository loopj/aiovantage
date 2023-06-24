"""Controller holding and managing Vantage temperature sensors."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import TemperatureInterface
from aiovantage.config_client.objects import Temperature

from .base import StatefulController


class TemperatureSensorsController(
    StatefulController[Temperature], TemperatureInterface
):
    """Controller holding and managing Vantage temperature sensors."""

    # Fetch the following object types from Vantage
    vantage_types = ("Temperature",)

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status = True
    enhanced_log_status_methods = ("Temperature.GetValue",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of a temperature sensor."""

        state: Dict[str, Any] = {
            "value": await TemperatureInterface.get_value(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a temperature sensor."""

        state: Dict[str, Any] = {}
        if status == "Temperature.GetValue":
            state["value"] = TemperatureInterface.parse_get_value_status(args)

        self.update_state(vid, state)
