"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface, InterfaceResponse, fixed_result


class SensorInterface(Interface):
    """Interface for querying and controlling sensors."""

    async def get_level(self, vid: int) -> Decimal:
        """Get the level of a sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevel
        response = await self.invoke(vid, "Sensor.GetLevel")
        return self.parse_get_level_response(response)

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevelHW
        response = await self.invoke(vid, "Sensor.GetLevelHW")
        return self.parse_get_level_response(response)

    @classmethod
    def parse_get_level_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Sensor.GetLevel' response."""
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        # -> S:STATUS <id> Sensor.GetLevel <level>
        # -> EL: <id> Sensor.GetLevel <level>
        return fixed_result(response)
