"""Controller holding and managing Vantage anemo (wind) sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import AnemoSensor

from .base import BaseController


class AnemoSensorsController(BaseController[AnemoSensor]):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    vantage_types = (AnemoSensor,)
    status_types = ("WIND",)

    @override
    async def fetch_object_state(self, obj: AnemoSensor) -> None:
        """Fetch the state properties of an anemo sensor."""
        state = {
            "speed": await obj.get_speed(),
        }

        self.update_state(obj.id, state)

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
