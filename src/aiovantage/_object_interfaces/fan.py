from enum import IntEnum

from .base import Interface, method


class FanInterface(Interface):
    """Fan object interface."""

    interface_name = "Fan"

    class FanSpeed(IntEnum):
        """Fan speed."""

        Off = 0
        Low = 1
        Medium = 2
        High = 3
        Max = 4
        Auto = 5

    # Properties
    speed: FanSpeed | None = None

    # Methods
    @method("GetSpeed", "GetSpeedHW", property="speed")
    async def get_speed(self, *, hw: bool = False) -> FanSpeed:
        """Get the speed of a fan.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The speed of the fan.
        """
        # INVOKE <id> Fan.GetSpeed
        # -> R:INVOKE <id> <speed> Fan.GetSpeed
        return await self.invoke("Fan.GetSpeedHW" if hw else "Fan.GetSpeed")

    @method("SetSpeed", "SetSpeedSW")
    async def set_speed(self, speed: FanSpeed, *, sw: bool = False) -> None:
        """Set the speed of a fan.

        Args:
            speed: The speed to set the fan to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Fan.SetSpeed <speed>
        # -> R:INVOKE <id> <rcode> Fan.SetSpeed <speed>
        await self.invoke("Fan.SetSpeedSW" if sw else "Fan.SetSpeed", speed)

    @method("IncreaseSpeed")
    async def increase_speed(self, vid: int) -> None:
        """Increase the speed of a fan."""
        # INVOKE <id> Fan.IncreaseSpeed
        # -> R:INVOKE <id> <rcode> Fan.IncreaseSpeed
        await self.invoke("Fan.IncreaseSpeed")

    @method("DecreaseSpeed")
    async def decrease_speed(self) -> None:
        """Decrease the speed of a fan."""
        # INVOKE <id> Fan.DecreaseSpeed
        # -> R:INVOKE <id> <rcode> Fan.DecreaseSpeed
        await self.invoke("Fan.DecreaseSpeed")
