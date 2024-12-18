"""Controller holding and managing Vantage omni sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.command_client.utils import parse_fixed_param
from aiovantage.objects import OmniSensor

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
        state = {
            "level": await self.get_level(obj, cached=False),
        }

        self.update_state(obj.vid, state)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *_args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        omni_sensor = self[vid]
        if method != omni_sensor.get.method:
            return

        state = {
            "level": self.parse_result(omni_sensor, result),
        }

        self.update_state(vid, state)

    async def get_level(self, obj: OmniSensor, cached: bool = True) -> int | Decimal:
        """Get the level of an OmniSensor.

        Args:
            obj: The OmniSensor object to get the level of.
            cached: Whether to use the cached value or fetch a new one.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> <method>
        # -> R:INVOKE <id> <value> <method>
        method = obj.get.method if cached else obj.get.method_hw
        response = await self.command_client.command("INVOKE", obj.vid, method)

        return self.parse_result(obj, response.args[1])

    @classmethod
    def parse_result(cls, sensor: OmniSensor, result: str) -> int | Decimal:
        """Parse an OmniSensor response, eg. 'PowerSensor.GetPower'."""
        # NOTE: This currently doesn't handle conversion formulas, or return_type
        level = parse_fixed_param(result)
        if sensor.get.formula.level_type == OmniSensor.ConversionType.INT:
            return int(level)

        return level
