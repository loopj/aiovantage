"""Controller holding and managing Vantage temperature sensors."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import TemperatureInterface
from aiovantage.config_client.objects import Temperature

from .base import BaseController, State


class TemperatureSensorsController(BaseController[Temperature], TemperatureInterface):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = ("Temperature",)
    """The Vantage object types that this controller will fetch."""

    enhanced_log_status_methods = ("Temperature.GetValue",)
    """Which status methods this controller handles from the Enhanced Log."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a temperature sensor."""
        return {
            "value": await TemperatureInterface.get_value(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a temperature sensor."""
        if status != "Temperature.GetValue":
            return None

        return {
            "value": TemperatureInterface.parse_get_value_status(args),
        }
