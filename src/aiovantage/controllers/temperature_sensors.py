"""Controller holding and managing Vantage temperature sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.models import Temperature
from aiovantage.object_interfaces import TemperatureInterface

from .base import BaseController


class TemperatureSensorsController(BaseController[Temperature]):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = ("Temperature",)
    status_types = ("TEMP",)

    @override
    async def fetch_object_state(self, obj: Temperature) -> None:
        """Fetch the state properties of a temperature sensor."""
        state = {
            "value": await TemperatureInterface.get_value(obj),
        }

        self.update_state(obj.id, state)

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
