"""Controller holding and managing Vantage light sensors."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import LightSensorInterface
from aiovantage.config_client.objects import LightSensor

from .base import BaseController


class LightSensorsController(BaseController[LightSensor], LightSensorInterface):
    """Controller holding and managing Vantage light sensors."""

    # Fetch the following object types from Vantage
    vantage_types = ("LightSensor",)

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status = True
    enhanced_log_status_methods = ("LightSensor.GetLevel",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of a light sensor."""

        state: Dict[str, Any] = {
            "level": await LightSensorInterface.get_level(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a light sensor."""

        state: Dict[str, Any] = {}
        if status == "LightSensor.GetLevel":
            state["level"] = LightSensorInterface.parse_get_level_status(args)

        self.update_state(vid, state)
