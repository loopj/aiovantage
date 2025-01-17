"""Interface for querying and controlling fans."""

from enum import IntEnum

from .base import Interface, method


class FanInterface(Interface):
    """Interface for querying and controlling fans."""

    class FanSpeed(IntEnum):
        """Fan speed."""

        OFF = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        MAX = 4
        AUTO = 5

    @method("Fan.GetSpeed")
    @method("Fan.GetSpeedHW")
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

    @method("Fan.SetSpeed")
    @method("Fan.SetSpeedSW")
    async def set_speed(self, speed: FanSpeed, *, sw: bool = False) -> None:
        """Set the speed of a fan.

        Args:
            speed: The speed to set the fan to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Fan.SetSpeed <speed>
        # -> R:INVOKE <id> <rcode> Fan.SetSpeed <speed>
        await self.invoke("Fan.SetSpeedSW" if sw else "Fan.SetSpeed", speed)

    @method("Fan.IncreaseSpeed")
    async def increase_speed(self) -> None:
        """Increase the speed of a fan."""
        # INVOKE <id> Fan.IncreaseSpeed
        # -> R:INVOKE <id> <rcode> Fan.IncreaseSpeed
        await self.invoke("Fan.IncreaseSpeed")

    @method("Fan.DecreaseSpeed")
    async def decrease_speed(self) -> None:
        """Decrease the speed of a fan."""
        # INVOKE <id> Fan.DecreaseSpeed
        # -> R:INVOKE <id> <rcode> Fan.DecreaseSpeed
        await self.invoke("Fan.DecreaseSpeed")
