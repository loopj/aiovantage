"""Controller holding and managing Vantage light sensors."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import LightSensorInterface
from aiovantage.config_client.objects import LightSensor

from .base import BaseController, State


class LightSensorsController(BaseController[LightSensor], LightSensorInterface):
    """Controller holding and managing Vantage light sensors."""

    # Fetch the following object types from Vantage
    vantage_types = ("LightSensor",)

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status_methods = ("LightSensor.GetLevel",)

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a light sensor."""
        return {
            "level": await LightSensorInterface.get_level(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a light sensor."""
        if status != "LightSensor.GetLevel":
            return None

        return {
            "level": LightSensorInterface.parse_get_level_status(args),
        }
