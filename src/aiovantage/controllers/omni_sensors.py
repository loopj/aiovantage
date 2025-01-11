"""Controller holding and managing Vantage omni sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.command_client.utils import parse_object_response
from aiovantage.errors import CommandError
from aiovantage.objects.omni_sensor import OmniSensor

from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    """Controller holding and managing Vantage omni sensors.

    Omni sensors are generic sensors objects which specify which methods to use
    when getting or setting data in their object definition, as well as the
    type of data and a conversion formula.
    """

    vantage_types = (OmniSensor,)
    interface_status_types = "*"

    @override
    async def fetch_object_state(self, obj: OmniSensor) -> None:
        """Fetch the state properties of an omni sensor."""
        try:
            self.update_state(obj.id, {"level": await obj.get_level_hw()})
        except CommandError:
            self._logger.debug("Failed to fetch state for OmniSensor %s", obj.id)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *_args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        omni_sensor = self[vid]
        if method != omni_sensor.get.method:
            return

        state = {
            "level": parse_object_response(result, as_type=Decimal),
        }

        self.update_state(vid, state)
