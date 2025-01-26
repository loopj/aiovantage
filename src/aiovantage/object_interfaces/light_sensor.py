"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from .base import Interface


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    method_signatures = {
        "LightSensor.GetLevel": Decimal,
        "LightSensor.GetLevelHW": Decimal,
    }

    async def get_level(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the level of a light sensor.

        Args:
            vid: The Vantage ID of the light sensor.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        return await self.invoke(
            vid, "LightSensor.GetLevelHW" if hw else "LightSensor.GetLevel"
        )

    async def set_level(self, vid: int, level: Decimal) -> None:
        """Set the level of a light sensor.

        Args:
            vid: The Vantage ID of the light sensor.
            level: The level to set, in foot-candles.
        """
        # INVOKE <id> LightSensor.SetLevel <level>
        # -> R:INVOKE <id> <rcode> LightSensor.SetLevel <level>
        await self.invoke(vid, "LightSensor.SetLevel", level)
