"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface
from .parsers import parse_fixed


class SensorInterface(Interface):
    """Interface for querying and controlling sensors."""

    response_parsers = {
        "Sensor.GetLevel": parse_fixed,
        "Sensor.GetLevelHW": parse_fixed,
    }

    async def get_level(self, vid: int) -> Decimal:
        """Get the level of a sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevel
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        response = await self.invoke(vid, "Sensor.GetLevel")
        return SensorInterface.parse_response(response, Decimal)

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevelHW
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevelHW
        response = await self.invoke(vid, "Sensor.GetLevelHW")
        return SensorInterface.parse_response(response, Decimal)
