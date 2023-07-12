"""Controller holding and managing Vantage anemo (wind) sensors."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import AnemoSensorInterface
from aiovantage.models import AnemoSensor

from .base import BaseController, State


class AnemoSensorsController(BaseController[AnemoSensor], AnemoSensorInterface):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    vantage_types = ("AnemoSensor",)
    """The Vantage object types that this controller will fetch."""

    enhanced_log_status_methods = ("AnemoSensor.GetSpeed",)
    """Which status methods this controller handles from the Enhanced Log."""

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
