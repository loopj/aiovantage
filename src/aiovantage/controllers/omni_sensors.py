"""Controller holding and managing Vantage omni sensors."""

from decimal import Decimal
from typing import Union

from typing_extensions import override

from aiovantage.command_client.object_interfaces.base import InterfaceResponse
from aiovantage.config_client.models.omni_sensor import ConversionType, OmniSensor

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
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of an omni sensor."""
        state = {
            "level": await self.get_level(vid),
        }

        self.update_state(vid, state)

    @override
    def handle_interface_status(self, status: InterfaceResponse) -> None:
        """Handle object interface status messages from the event stream."""
        omni_sensor = self[status.vid]
        if status.method != omni_sensor.get.method:
            return

        state = {
            "level": self.parse_get_level_status(omni_sensor, status),
        }

        self.update_state(status.vid, state)

    async def get_level(self, vid: int, cached: bool = False) -> Union[int, Decimal]:
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

        # Convert the level to the correct type
        if omni_sensor.get.formula.return_type == ConversionType.FIXED:
            level = Decimal(response.args[1])
            if omni_sensor.get.formula.level_type == ConversionType.INT:
                return int(level)

            return level

        if omni_sensor.get.formula.return_type == ConversionType.INT:
            level = Decimal(response.args[1]) / 1000
            if omni_sensor.get.formula.level_type == ConversionType.INT:
                return int(level)

            return level

        raise ValueError(f"Unknown return type {omni_sensor.get.formula.return_type}")

    @classmethod
    def parse_get_level_status(
        cls, omni_sensor: OmniSensor, status: InterfaceResponse
    ) -> Union[int, Decimal]:
        """Parse an OmniSensor 'GetLevel' event, eg. 'PowerSensor.GetPower'."""
        # -> S:STATUS <id> <method> <value>
        # -> EL: <id> <method> <value>
        level = Decimal(status.result) / 1000
        if omni_sensor.get.formula.level_type == ConversionType.INT:
            return int(level)

        return level
