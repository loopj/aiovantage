"""Interface for querying and controlling light sensors."""

from decimal import Decimal

from .base import Interface, method


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    interface_name = "LightSensor"

    # Properties
    level: Decimal | None = None

    # Methods
    @method("GetLevel", "GetLevelHW", property="level")
    async def get_level(self, *, hw: bool = False) -> Decimal:
        """Get the level of a light sensor.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        return await self.invoke(
            "LightSensor.GetLevelHW" if hw else "LightSensor.GetLevel"
        )

    @method("SetLevel", "SetLevelSW")
    async def set_level(self, level: Decimal) -> None:
        """Set the level of a light sensor.

        Args:
            level: The level to set, in foot-candles.
        """
        # INVOKE <id> LightSensor.SetLevel <level>
        # -> R:INVOKE <id> <rcode> LightSensor.SetLevel <level>
        await self.invoke("LightSensor.SetLevel", level)
