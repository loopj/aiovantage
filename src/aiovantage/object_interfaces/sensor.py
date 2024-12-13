"""Interface for querying and controlling sensors."""

from decimal import Decimal

from aiovantage.object_interfaces.base import Interface


class SensorInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Sensor.GetLevel": Decimal,
        "Sensor.GetLevelHW": Decimal,
    }

    level: Decimal | None = None

    async def get_level(self) -> Decimal:
        """Get the level of a sensor, using cached value if available.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevel
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        return await self.invoke("Sensor.GetLevel", as_type=Decimal)

    async def get_level_hw(self) -> Decimal:
        """Get the level of a sensor directly from the hardware.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevelHW
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevelHW
        return await self.invoke("Sensor.GetLevelHW", as_type=Decimal)
