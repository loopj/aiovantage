"""Controller holding and managing Vantage light sensors."""

from decimal import Decimal
from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import LightSensorInterface
from aiovantage.models import LightSensor

from .base import BaseController, State


class LightSensorsController(BaseController[LightSensor], LightSensorInterface):
    """Controller holding and managing Vantage light sensors."""

    vantage_types = ("LightSensor",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("LIGHT",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a light sensor."""
        return {
            "level": await LightSensorInterface.get_level(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a light sensor."""
        if status != "LIGHT":
            return None

        # STATUS LIGHT
        # -> S:LIGHT <id> <level>
        return {
            "level": Decimal(args[0]),
        }
