"""Controller holding and managing Vantage anemo (wind) sensors."""

from decimal import Decimal
from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import AnemoSensorInterface
from aiovantage.models import AnemoSensor

from .base import BaseController, State


class AnemoSensorsController(BaseController[AnemoSensor], AnemoSensorInterface):
    """Controller holding and managing Vantage anemo (wind) sensors."""

    vantage_types = ("AnemoSensor",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("WIND",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of an anemo sensor."""
        return {
            "speed": await AnemoSensorInterface.get_speed(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a wind sensor."""
        if status != "WIND":
            return None

        # STATUS WIND
        # -> S:WIND <id> <wind_speed>
        return {
            "speed": Decimal(args[0]),
        }
