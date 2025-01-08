"""Controller holding and managing Vantage temperature sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import Temperature

from .base import BaseController


class TemperatureSensorsController(BaseController[Temperature]):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = (Temperature,)
    status_types = ("TEMP",)
    fetch_properties = ("value",)

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
