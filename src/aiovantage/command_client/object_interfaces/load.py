"""Interface for querying and controlling loads."""

from decimal import Decimal
from enum import IntEnum
from typing import Optional, Union

from .base import Interface, InterfaceResponse, fixed_result


class LoadInterface(Interface):
    """Interface for querying and controlling loads."""

    class RampType(IntEnum):
        """The type of ramp to perform."""

        UP = 5
        DOWN = 4
        OPPOSITE = 3
        STOP = 2
        FIXED = 6
        VARIABLE = 7
        ADJUST = 8

    async def set_level(self, vid: int, level: Union[float, Decimal]) -> None:
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
        """Get the level of a load.

        Args:
            vid: The Vantage ID of the load.

        Returns:
            The level of the load, as a percentage (0-100).
        """
        # INVOKE <id> Load.GetLevel
        response = await self.invoke(vid, "Load.GetLevel")
        return self.parse_get_level_response(response)

    async def ramp(
        self,
        vid: int,
        cmd: RampType = RampType.FIXED,
        time: Union[float, Decimal] = 0,
        level: Union[float, Decimal] = 0,
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

    async def turn_on(
        self,
        vid: int,
        transition: Optional[float] = None,
        level: Optional[float] = None,
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

    async def turn_off(self, vid: int, transition: Optional[float] = None) -> None:
        """Turn off a load with an optional transition time.

        Args:
            vid: The Vantage ID of the load.
            transition: The time in seconds to ramp the load down, defaults to immediate.
        """
        if transition is None:
            return await self.set_level(vid, 0)

        await self.ramp(vid, time=transition, level=0)

    @classmethod
    def parse_get_level_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Load.GetLevel' response."""
        # -> R:INVOKE <id> <level (0.000-100.000)> Load.GetLevel
        # -> S:STATUS <id> Load.GetLevel <level (0-100000)>
        # -> EL: <id> Load.GetLevel <level (0-100000)>
        return fixed_result(response)
