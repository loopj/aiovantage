"""Controller holding and managing Vantage light sensors."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import LightSensorInterface
from aiovantage.models import LightSensor

from .base import BaseController, State


class LightSensorsController(BaseController[LightSensor], LightSensorInterface):
    """Controller holding and managing Vantage light sensors."""

    vantage_types = ("LightSensor",)
    """The Vantage object types that this controller will fetch."""

    enhanced_log_status_methods = ("LightSensor.GetLevel",)
    """Which status methods this controller handles from the Enhanced Log."""

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
