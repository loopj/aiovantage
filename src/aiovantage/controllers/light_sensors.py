"""Controller holding and managing Vantage light sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.models import LightSensor
from aiovantage.object_interfaces import (
    LightSensorInterface,
    SensorInterface,
)

from .base import BaseController


class LightSensorsController(
    BaseController[LightSensor], LightSensorInterface, SensorInterface
):
    """Controller holding and managing Vantage light sensors."""

    vantage_types = ("LightSensor",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("LIGHT",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a light sensor."""
        state = {
            "level": await LightSensorInterface.get_level(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "LIGHT":
            return

        # STATUS LIGHT
        # -> S:LIGHT <id> <level>
        state = {
            "level": Decimal(args[0]),
        }

        self.update_state(vid, state)
