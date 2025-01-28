"""Controller holding and managing Vantage omni sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.command_client.types import converter
from aiovantage.objects.omni_sensor import OmniSensor

from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    """Controller holding and managing Vantage omni sensors.

    Omni sensors are generic sensors objects which specify which methods to use
    when getting or setting data in their object definition, as well as the
    type of data and a conversion formula.
    """

    vantage_types = ("OmniSensor",)
    """The Vantage object types that this controller will fetch."""

    interface_status_types = "*"
    """Which object interface status messages this controller handles, if any."""

    @override
    async def fetch_object_state(self, obj: OmniSensor) -> None:
        """Fetch the state properties of an omni sensor."""
        state = {
            "level": await obj.get_level(hw=True),
        }

        self.update_state(obj, state)

    @override
    def handle_interface_status(
        self, obj: OmniSensor, method: str, result: str, *_args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != obj.get.method:
            return

        state = {
            "level": converter.deserialize(Decimal, result),
        }

        self.update_state(obj, state)
