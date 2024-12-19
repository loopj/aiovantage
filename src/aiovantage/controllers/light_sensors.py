"""Controller holding and managing Vantage light sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import LightSensor

from .base import BaseController


class LightSensorsController(BaseController[LightSensor]):
    """Controller holding and managing Vantage light sensors."""

    vantage_types = (LightSensor,)
    status_types = ("LIGHT",)

    @override
    async def fetch_object_state(self, obj: LightSensor) -> None:
        """Fetch the state properties of a light sensor."""
        state = {
            "level": await obj.get_level(),
        }

        self.update_state(obj.id, state)

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
