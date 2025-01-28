"""Controller holding and managing Vantage light sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import LightSensor

from .base import BaseController


class LightSensorsController(BaseController[LightSensor]):
    """Controller holding and managing Vantage light sensors."""

    vantage_types = ("LightSensor",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("LIGHT",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    def handle_status(self, obj: LightSensor, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "LIGHT":
            return

        # STATUS LIGHT
        # -> S:LIGHT <id> <level>
        state = {
            "level": Decimal(args[0]),
        }

        self.update_state(obj, state)
