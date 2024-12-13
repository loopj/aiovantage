"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from aiovantage.object_interfaces.base import Interface


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    method_signatures = {
        "LightSensor.GetLevel": Decimal,
        "LightSensor.GetLevelHW": Decimal,
    }

    level: Decimal | None = None

    async def get_level(self) -> Decimal:
        """Get the level of a light sensor, using cached value if available.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        return await self.invoke("LightSensor.GetLevel", as_type=Decimal)

    async def get_level_hw(self) -> Decimal:
        """Get the level of a light sensor directly from the hardware.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevelHW
        # -> R:INVOKE <id> <level> LightSensor.GetLevelHW
        return await self.invoke("LightSensor.GetLevelHW", as_type=Decimal)
