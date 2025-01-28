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
            "level": await self.get_level(obj.vid, cached=False),
        }

        self.update_state(obj.vid, state)

    @override
    def handle_interface_status(
        self, obj: OmniSensor, method: str, result: str, *_args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != obj.get.method:
            return

        state = {
            "level": self.parse_result(obj, result),
        }

        self.update_state(obj.vid, state)

    async def get_level(self, vid: int, cached: bool = True) -> int | Decimal:
        """Get the level of an OmniSensor.

        Args:
            vid: The ID of the sensor.
            cached: Whether to use the cached value or fetch a new one.

        Returns:
            The level of the sensor.
        """
        omni_sensor = self[vid]

        # INVOKE <id> <method>
        # -> R:INVOKE <id> <value> <method>
        method = omni_sensor.get.method if cached else omni_sensor.get.method_hw
        response = await self.command_client.command("INVOKE", vid, method)

        return self.parse_result(omni_sensor, response.args[1])

    @classmethod
    def parse_result(cls, sensor: OmniSensor, result: str) -> int | Decimal:
        """Parse an OmniSensor response, eg. 'PowerSensor.GetPower'."""
        return converter.deserialize(Decimal, result)
