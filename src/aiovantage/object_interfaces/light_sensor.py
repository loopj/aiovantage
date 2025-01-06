"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from .base import Interface, method


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    # Properties
    level: int | Decimal | None = None

    # Methods
    @method("LightSensor.GetLevel", property="level")
    async def get_level(self) -> Decimal:
        """Get the level of a light sensor, using cached value if available.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        return await self.invoke("LightSensor.GetLevel")

    @method("LightSensor.GetLevelHW")
    async def get_level_hw(self) -> Decimal:
        """Get the level of a light sensor directly from the hardware.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevelHW
        # -> R:INVOKE <id> <level> LightSensor.GetLevelHW
        return await self.invoke("LightSensor.GetLevelHW")

    @method("LightSensor.SetLevel")
    async def set_level(self, level: Decimal) -> None:
        """Set the level of a light sensor.

        Args:
            level: The level to set, in foot-candles.
        """
        # INVOKE <id> LightSensor.SetLevel <level>
        # -> R:INVOKE <id> <rcode> LightSensor.SetLevel <level>
        await self.invoke("LightSensor.SetLevel", level)
