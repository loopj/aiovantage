"""Controller holding and managing Vantage temperature sensors."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import AnemoSensorInterface, SensorInterface
from aiovantage.config_client.objects import AnemoSensor

from .base import StatefulController


class AnemoSensorsController(
    StatefulController[AnemoSensor], AnemoSensorInterface, SensorInterface
):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    # Fetch the following object types from Vantage
    vantage_types = ("AnemoSensor",)

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status = True
    enhanced_log_status_methods = ("AnemoSensor.GetSpeed",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of an anemo sensor."""

        state: Dict[str, Any] = {
            "speed": await AnemoSensorInterface.get_speed(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for an anemo sensor."""

        state: Dict[str, Any] = {}
        if status == "AnemoSensor.GetSpeed":
            state["speed"] = AnemoSensorInterface.parse_get_speed_status(args)

        self.update_state(vid, state)
