"""Controller holding and managing Vantage anemo (wind) sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.command_client.object_interfaces import (
    AnemoSensorInterface,
    SensorInterface,
)
from aiovantage.models import AnemoSensor

from .base import BaseController


class AnemoSensorsController(
    BaseController[AnemoSensor], AnemoSensorInterface, SensorInterface
):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    vantage_types = ("AnemoSensor",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("WIND",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of an anemo sensor."""
        state = {
            "speed": await AnemoSensorInterface.get_speed(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        if status != "WIND":
            return

        # STATUS WIND
        # -> S:WIND <id> <wind_speed>
        state = {
            "speed": Decimal(args[0]),
        }

        self.update_state(vid, state)
