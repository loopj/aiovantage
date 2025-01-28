"""Controller holding and managing Vantage anemo (wind) sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import AnemoSensor

from .base import BaseController


class AnemoSensorsController(BaseController[AnemoSensor]):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    vantage_types = ("AnemoSensor",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("WIND",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    def handle_status(self, obj: AnemoSensor, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        if status != "WIND":
            return

        # STATUS WIND
        # -> S:WIND <id> <wind_speed>
        state = {
            "speed": Decimal(args[0]),
        }

        self.update_state(obj, state)
