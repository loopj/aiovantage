"""Controller holding and managing Vantage omni sensors."""

from decimal import Decimal
from typing import Sequence, Union

from typing_extensions import override

from aiovantage.config_client.models.omni_sensor import ConversionType, OmniSensor

from .base import BaseController, State


class OmniSensorsController(BaseController[OmniSensor]):
    """Controller holding and managing Vantage omni sensors.

    Omni sensors are generic sensors objects which specify which methods to use
    when getting or setting data in their object definition, as well as the
    type of data and a conversion formula.
    """

    vantage_types = ("OmniSensor",)
    """The Vantage object types that this controller will fetch."""

    object_status = True
    """Should this controller subscribe to object status events."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of an omni sensor."""
        return {
            "level": await self.get_level(vid),
        }

    @override
    def parse_object_update(self, vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for an omni sensor."""
        omni_sensor = self[vid]
        if status != omni_sensor.get.method:
            return None

        return {
            "level": self.parse_get_level_status(omni_sensor, args),
        }

    async def get_level(self, vid: int, cached: bool = False) -> Union[int, Decimal]:
        """Get the level of an OmniSensor.

        Args:
            vid: The ID of the sensor.
            cached: Whether to use the cached value or fetch a new one.

        Returns:
            The level of the sensor.
        """
        # Figure out which get method to use, hardware or software (cached)
        omni_sensor = self[vid]
        method = omni_sensor.get.method if cached else omni_sensor.get.method_hw

        # INVOKE <id> <method>
        # -> R:INVOKE <id> <value> <method>
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
        cls, omni_sensor: OmniSensor, args: Sequence[str]
    ) -> Union[int, Decimal]:
        """Parse an OmniSensor 'GetLevel' event, eg. 'PowerSensor.GetPower'."""
        # ELLOG STATUS ON
        # -> EL: <id> <method> <value>
        # STATUS ADD <id>
        # -> S:STATUS <id> <method> <value>
        level = Decimal(args[0]) / 1000
        if omni_sensor.get.formula.level_type == ConversionType.INT:
            return int(level)

        return level
