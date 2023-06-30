"""Controller holding and managing Vantage anemo (wind) sensors."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import AnemoSensorInterface
from aiovantage.config_client.objects import AnemoSensor

from .base import BaseController, State


class AnemoSensorsController(BaseController[AnemoSensor], AnemoSensorInterface):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    # Fetch the following object types from Vantage
    vantage_types = ("AnemoSensor",)

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status_methods = ("AnemoSensor.GetSpeed",)

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of an anemo sensor."""
        return {
            "speed": await AnemoSensorInterface.get_speed(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for an anemo sensor."""
        if status != "AnemoSensor.GetSpeed":
            return None

        return {
            "speed": AnemoSensorInterface.parse_get_speed_status(args),
        }
