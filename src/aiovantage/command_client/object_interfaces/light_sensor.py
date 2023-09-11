"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from .base import Interface
from .parsers import parse_fixed


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    response_parsers = {
        "LightSensor.GetLevel": parse_fixed,
        "LightSensor.GetLevelHW": parse_fixed,
    }

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
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        return await self.invoke(vid, "LightSensor.GetLevel", as_type=Decimal)

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a light sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the light sensor.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevelHW
        # -> R:INVOKE <id> <level> LightSensor.GetLevelHW
        return await self.invoke(vid, "LightSensor.GetLevelHW", as_type=Decimal)
