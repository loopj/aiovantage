"""Controller holding and managing Vantage temperature sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.command_client.object_interfaces import TemperatureInterface
from aiovantage.models import Temperature

from .base import BaseController


class TemperatureSensorsController(BaseController[Temperature], TemperatureInterface):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = ("Temperature",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("TEMP",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a temperature sensor."""
        state = {
            "value": await TemperatureInterface.get_value(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        if status != "TEMP":
            return

        # STATUS TEMP
        # -> S:TEMP <id> <temp>
        state = {
            "value": Decimal(args[0]),
        }

        self.update_state(vid, state)
