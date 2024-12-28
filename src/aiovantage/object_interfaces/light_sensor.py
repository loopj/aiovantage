"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from .base import Interface


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    method_signatures = {
        "LightSensor.GetLevel": Decimal,
        "LightSensor.GetLevelHW": Decimal,
    }

    # Status properties
    level: int | Decimal | None = None  # "LightSensor.GetLevel"

    # Methods
    async def get_level(self) -> Decimal:
        """Get the level of a light sensor, using cached value if available.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        return await self.invoke("LightSensor.GetLevel")

    async def get_level_hw(self) -> Decimal:
        """Get the level of a light sensor directly from the hardware.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevelHW
        # -> R:INVOKE <id> <level> LightSensor.GetLevelHW
        return await self.invoke("LightSensor.GetLevelHW")

    async def set_level(self, level: Decimal) -> None:
        """Set the level of a light sensor.

        Args:
            level: The level to set, in foot-candles.
        """
        # INVOKE <id> LightSensor.SetLevel <level>
        # -> R:INVOKE <id> <rcode> LightSensor.SetLevel <level>
        await self.invoke("LightSensor.SetLevel", level)
