"""Controller holding and managing Vantage temperature sensors."""

from decimal import Decimal
from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import TemperatureInterface
from aiovantage.models import Temperature

from .base import BaseController, State


class TemperatureSensorsController(BaseController[Temperature], TemperatureInterface):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = ("Temperature",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("TEMP",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a temperature sensor."""
        return {
            "value": await TemperatureInterface.get_value(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a temperature sensor."""
        if status != "TEMP":
            return None

        # STATUS TEMP
        # -> S:TEMP <id> <temp>
        return {
            "value": Decimal(args[0]),
        }
