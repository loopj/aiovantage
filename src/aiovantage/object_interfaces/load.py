"""Interface for querying and controlling loads."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class LoadInterface(Interface):
    """Interface for querying and controlling loads."""

    class RampType(IntEnum):
        """The type of ramp to perform."""

        Up = 5
        Down = 4
        Opposite = 3
        Stop = 2
        Fixed = 6
        Variable = 7
        Adjust = 8

    method_signatures = {
        "Load.GetLevel": Decimal,
        "Load.GetLevelHW": Decimal,
    }

    async def set_level(self, vid: int, level: float | Decimal) -> None:
        """Set the level of a load.

        Args:
            vid: The Vantage ID of the load.
            level: The level to set the load to (0-100).
        """
        # Clamp level to 0-100
        level = max(min(level, 100), 0)

        # INVOKE <id> Load.SetLevel <level (0-100)>
        # -> R:INVOKE <id> <rcode> Load.SetLevel <level (0-100)>
        await self.invoke(vid, "Load.SetLevel", level)

    async def get_level(self, vid: int) -> Decimal:
        """Get the level of a load, using cached value if available.

        Args:
            vid: The Vantage ID of the load.

        Returns:
            The level of the load, as a percentage (0-100).
        """
        # INVOKE <id> Load.GetLevel
        # -> R:INVOKE <id> <level (0.000-100.000)> Load.GetLevel
        return await self.invoke(vid, "Load.GetLevel", as_type=Decimal)

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a load directly from the hardware.

        Args:
            vid: The Vantage ID of the load.

        Returns:
            The level of the load, as a percentage (0-100).
        """
        # INVOKE <id> Load.GetLevelHW
        # -> R:INVOKE <id> <level (0.000-100.000)> Load.GetLevelHW
        return await self.invoke(vid, "Load.GetLevelHW", as_type=Decimal)

    async def ramp(
        self,
        vid: int,
        cmd: RampType = RampType.Fixed,
        time: float | Decimal = 0,
        level: float | Decimal = 0,
    ) -> None:
        """Ramp a load to a level over a number of seconds.

        Args:
            vid: The Vantage ID of the load.
            cmd: The type of ramp to perform.
            time: The number of seconds to ramp the load over.
            level: The level to ramp the load to (0-100).
        """
        # Clamp level to 0-100
        level = max(min(level, 100), 0)

        # INVOKE <id> Load.Ramp <cmd> <time> <level>
        # -> R:INVOKE <id> <rcode> Load.Ramp <cmd> <time> <level>
        await self.invoke(vid, "Load.Ramp", cmd, time, level)

    # Additional convenience methods, not part of the Vantage API
    async def turn_on(
        self, vid: int, transition: float | None = None, level: float | None = None
    ) -> None:
        """Turn on a load with an optional transition time.

        Args:
            vid: The Vantage ID of the load.
            transition: The time in seconds to transition to the new level, defaults to immediate.
            level: The level to set the load to (0-100), defaults to 100.
        """
        if level is None:
            level = 100

        if transition is None:
            return await self.set_level(vid, level)

        await self.ramp(vid, time=transition, level=level)

    async def turn_off(self, vid: int, transition: float | None = None) -> None:
        """Turn off a load with an optional transition time.

        Args:
            vid: The Vantage ID of the load.
            transition: The time in seconds to ramp the load down, defaults to immediate.
        """
        if transition is None:
            return await self.set_level(vid, 0)

        await self.ramp(vid, time=transition, level=0)
