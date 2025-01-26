"""Interface for querying and controlling fans."""

from enum import IntEnum

from .base import Interface


class FanInterface(Interface):
    """Interface for querying and controlling fans."""

    class FanSpeed(IntEnum):
        """Fan speed."""

        Off = 0
        Low = 1
        Medium = 2
        Hight = 3
        Max = 4
        Auto = 5

    method_signatures = {
        "Fan.GetSpeed": FanSpeed,
        "Fan.GetSpeedHW": FanSpeed,
    }

    async def get_speed(self, vid: int, *, hw: bool = False) -> FanSpeed:
        """Get the speed of a fan.

        Args:
            vid: The Vantage ID of the fan.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The speed of the fan.
        """
        # INVOKE <id> Fan.GetSpeed
        # -> R:INVOKE <id> <speed> Fan.GetSpeed
        return await self.invoke(vid, "Fan.GetSpeedHW" if hw else "Fan.GetSpeed")

    async def set_speed(self, vid: int, speed: FanSpeed, *, sw: bool = False) -> None:
        """Set the speed of a fan.

        Args:
            vid: The Vantage ID of the fan.
            speed: The speed to set the fan to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Fan.SetSpeed <speed>
        # -> R:INVOKE <id> <rcode> Fan.SetSpeed <speed>
        await self.invoke(vid, "Fan.SetSpeedSW" if sw else "Fan.SetSpeed", speed)

    async def increase_speed(self, vid: int) -> None:
        """Increase the speed of a fan.

        Args:
            vid: The Vantage ID of the fan.
        """
        # INVOKE <id> Fan.IncreaseSpeed
        # -> R:INVOKE <id> <rcode> Fan.IncreaseSpeed
        await self.invoke(vid, "Fan.IncreaseSpeed")

    async def decrease_speed(self, vid: int) -> None:
        """Decrease the speed of a fan.

        Args:
            vid: The Vantage ID of the fan.
        """
        # INVOKE <id> Fan.DecreaseSpeed
        # -> R:INVOKE <id> <rcode> Fan.DecreaseSpeed
        await self.invoke(vid, "Fan.DecreaseSpeed")
