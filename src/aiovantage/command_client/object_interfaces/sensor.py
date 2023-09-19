"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface


class SensorInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Sensor.GetLevel": Decimal,
        "Sensor.GetLevelHW": Decimal,
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
        return await self.invoke(vid, "Sensor.GetLevel", as_type=Decimal)

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevelHW
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevelHW
        return await self.invoke(vid, "Sensor.GetLevelHW", as_type=Decimal)
