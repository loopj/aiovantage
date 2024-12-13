"""Interface for querying and controlling loads."""

from decimal import Decimal
from enum import IntEnum

from aiovantage.object_interfaces.base import Interface
from aiovantage.object_interfaces.interface_classes import WidgetPrecludable


class LoadInterface(Interface, WidgetPrecludable):
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

    level: float | None = None

    async def set_level(self, level: float | Decimal) -> None:
        """Set the level of a load.

        Args:
            level: The level to set the load to (0-100).
        """
        # Clamp level to 0-100
        level = max(min(level, 100), 0)

        # INVOKE <id> Load.SetLevel <level (0-100)>
        # -> R:INVOKE <id> <rcode> Load.SetLevel <level (0-100)>
        await self.invoke("Load.SetLevel", level)

    async def get_level(self) -> Decimal:
        """Get the level of a load, using cached value if available.

        Returns:
            The level of the load, as a percentage (0-100).
        """
        # INVOKE <id> Load.GetLevel
        # -> R:INVOKE <id> <level (0.000-100.000)> Load.GetLevel
        return await self.invoke("Load.GetLevel", as_type=Decimal)

    async def get_level_hw(self) -> Decimal:
        """Get the level of a load directly from the hardware.

        Returns:
            The level of the load, as a percentage (0-100).
        """
        # INVOKE <id> Load.GetLevelHW
        # -> R:INVOKE <id> <level (0.000-100.000)> Load.GetLevelHW
        return await self.invoke("Load.GetLevelHW", as_type=Decimal)

    async def ramp(
        self,
        cmd: RampType = RampType.Fixed,
        time: float | Decimal = 0,
        level: float | Decimal = 0,
    ) -> None:
        """Ramp a load to a level over a number of seconds.

        Args:
            cmd: The type of ramp to perform.
            time: The number of seconds to ramp the load over.
            level: The level to ramp the load to (0-100).
        """
        # Clamp level to 0-100
        level = max(min(level, 100), 0)

        # INVOKE <id> Load.Ramp <cmd> <time> <level>
        # -> R:INVOKE <id> <rcode> Load.Ramp <cmd> <time> <level>
        await self.invoke("Load.Ramp", cmd, time, level)

    # Additional convenience methods, not part of the Vantage API
    async def turn_on(
        self, transition: float | None = None, level: float | None = None
    ) -> None:
        """Turn on a load with an optional transition time.

        Args:
            transition: The time in seconds to transition to the new level, defaults to immediate.
            level: The level to set the load to (0-100), defaults to 100.
        """
        if level is None:
            level = 100

        if transition is None:
            return await self.set_level(level)

        await self.ramp(time=transition, level=level)

    async def turn_off(self, transition: float | None = None) -> None:
        """Turn off a load with an optional transition time.

        Args:
            transition: The time in seconds to ramp the load down, defaults to immediate.
        """
        if transition is None:
            return await self.set_level(0)

        await self.ramp(time=transition, level=0)

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
