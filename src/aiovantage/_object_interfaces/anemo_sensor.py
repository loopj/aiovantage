from decimal import Decimal

from typing_extensions import override

from .base import Interface, method


class AnemoSensorInterface(Interface):
    """Anemo sensor object interface."""

    interface_name = "AnemoSensor"

    # Properties
    speed: Decimal | None = None

    # Methods
    @method("GetSpeed", "GetSpeedHW", property="speed")
    async def get_speed(self, *, hw: bool = False) -> Decimal:
        """Get the speed of an anemo sensor.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        return await self.invoke(
            "AnemoSensor.GetSpeedHW" if hw else "AnemoSensor.GetSpeed"
        )

    @method("SetSpeed", "SetSpeedSW")
    async def set_speed(self, speed: Decimal, *, sw: bool = False) -> None:
        """Set the speed of an anemo sensor.

        Args:
            speed: The speed to set, in mph.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> AnemoSensor.SetSpeed <speed>
        # -> R:INVOKE <id> <rcode> AnemoSensor.SetSpeed <speed>
        await self.invoke(
            "AnemoSensor.SetSpeedSW" if sw else "AnemoSensor.SetSpeed", speed
        )

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "WIND":
            # STATUS WIND
            # -> S:WIND <id> <wind_speed>
            return self.update_properties({"speed": Decimal(args[0])})

        return super().handle_category_status(category, *args)
