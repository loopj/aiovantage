from decimal import Decimal

from typing_extensions import override

from .base import Interface, method


class LightSensorInterface(Interface):
    """Light sensor object interface."""

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

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "LIGHT":
            # STATUS LIGHT
            # -> S:LIGHT <id> <level>
            return self.update_properties({"level": Decimal(args[0])})

        return super().handle_category_status(category, *args)
