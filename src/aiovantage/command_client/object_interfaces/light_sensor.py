"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from .base import Interface, InterfaceResponse, fixed_result


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    async def get_level(self, vid: int) -> Decimal:
        """Get the level of a light sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the light sensor.

        Returns:
            The level of the light sensor, in foot-candles.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        response = await self.invoke(vid, "LightSensor.GetLevel")
        return self.parse_get_level_response(response)

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a light sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the light sensor.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevelHW
        response = await self.invoke(vid, "LightSensor.GetLevelHW")
        return self.parse_get_level_response(response)

    @classmethod
    def parse_get_level_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'LightSensor.GetLevel' response."""
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        # -> S:STATUS <id> LightSensor.GetLevel <level>
        # -> EL: <id> LightSensor.GetLevel <level>
        return fixed_result(response)
