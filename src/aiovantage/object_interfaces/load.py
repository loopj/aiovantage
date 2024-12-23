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

    class AlertState(IntEnum):
        """The alert state of the load."""

        Clear = 0
        Overload = 1
        BulbChange = 2
        WrongType = 3
        DCCurrent = 4
        ShortCircuit = 5

    class DimmingConfig(IntEnum):
        """The type of dimming the load should perform."""

        Manual = 0
        Forward = 1
        Reverse = 2
        Auto = 3

    method_signatures = {
        "Load.GetLevel": Decimal,
        "Load.GetLevelHW": Decimal,
    }

    # Properties
    level: Decimal | None = None

    # Methods
    async def set_level(self, level: float | Decimal) -> None:
        """Set the level of a load.

        Args:
            level: The level to set the load to (0-100).
        """
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
        self, cmd: RampType, ramptime: float | Decimal, finallevel: float | Decimal
    ) -> None:
        """Ramp a load to a level over a number of seconds.

        Args:
            cmd: The type of ramp to perform.
            ramptime: The number of seconds to ramp the load over.
            finallevel: The level to ramp the load to (0-100).
        """
        # INVOKE <id> Load.Ramp <cmd> <time> <level>
        # -> R:INVOKE <id> <rcode> Load.Ramp <cmd> <time> <level>
        await self.invoke("Load.Ramp", cmd, ramptime, finallevel)

    async def set_profile(self, profile: int) -> None:
        """Set the id of the power profile used by this load.

        Args:
            profile: The power profile id to set the load to.
        """
        # INVOKE <id> Load.SetProfile <profile>
        # -> R:INVOKE <id> <rcode> Load.SetProfile <profile>
        await self.invoke("Load.SetProfile", profile)

    async def get_profile(self) -> int:
        """Get the id of the power profile used by this load.

        Returns:
            The power profile id used by the load.
        """
        # INVOKE <id> Load.GetProfile
        # -> R:INVOKE <id> <profile> Load.GetProfile
        return await self.invoke("Load.GetProfile", as_type=int)

    async def get_override_level(self) -> Decimal:
        """Get the override level of a load.

        Returns:
            The override level of the load, as a percentage (0-100).
        """
        # INVOKE <id> Load.GetOverrideLevel
        # -> R:INVOKE <id> <level (0.000-100.000)> Load.GetOverrideLevel
        return await self.invoke("Load.GetOverrideLevel", as_type=Decimal)

    async def set_level_sw(self, level: float | Decimal) -> None:
        """Set the cached level of a load.

        Args:
            level: The level to set the load to (0-100).
        """
        # INVOKE <id> Load.SetLevelSW <level (0-100)>
        # -> R:INVOKE <id> <rcode> Load.SetLevelSW <level (0-100)>
        await self.invoke("Load.SetLevelSW", level)

    async def ramp_auto_off(
        self,
        cmd: RampType,
        ramptime: float | Decimal,
        finallevel: float | Decimal,
        offcmd: RampType,
        offramptime: float | Decimal,
        offtimeout: float | Decimal,
    ) -> None:
        """Ramp a load to a level over a number of seconds, then ramp off after a timeout.

        Args:
            cmd: The type of ramp to perform.
            ramptime: The number of seconds to ramp the load over.
            finallevel: The level to ramp the load to (0-100).
            offcmd: The type of ramp to perform to turn the load off.
            offramptime: The number of seconds to ramp the load off over.
            offtimeout: The number of seconds to wait before turning the load off.
        """
        # INVOKE <id> Load.RampAutoOff <cmd> <time> <level> <offcmd> <offtime> <offlevel>
        # -> R:INVOKE <id> <rcode> Load.RampAutoOff <cmd> <time> <level> <offcmd> <offtime> <offlevel>
        await self.invoke(
            "Load.RampAutoOff",
            cmd,
            ramptime,
            finallevel,
            offcmd,
            offramptime,
            offtimeout,
        )

    async def get_alert_state(self) -> AlertState:
        """Get the alert state of a load.

        Returns:
            The alert state of the load.
        """
        # INVOKE <id> Load.GetAlertState
        # -> R:INVOKE <id> <alert state> Load.GetAlertState
        return await self.invoke("Load.GetAlertState", as_type=LoadInterface.AlertState)

    async def set_alert_state_sw(self, alert_state: AlertState) -> None:
        """Set the cached alert state of a load.

        Args:
            alert_state: The alert state to set the load to.
        """
        # INVOKE <id> Load.SetAlertStateSW <alert state>
        # -> R:INVOKE <id> <rcode> Load.SetAlertStateSW <alert state>
        await self.invoke("Load.SetAlertStateSW", alert_state)

    async def get_dimming_config(self) -> DimmingConfig:
        """Get the dimming configuration of a load.

        Returns:
            The dimming configuration of the load.
        """
        # INVOKE <id> Load.GetDimmingConfig
        # -> R:INVOKE <id> <dimming config> Load.GetDimmingConfig
        return await self.invoke(
            "Load.GetDimmingConfig", as_type=LoadInterface.DimmingConfig
        )

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

        await self.ramp(LoadInterface.RampType.Fixed, transition, level)

    async def turn_off(self, transition: float | None = None) -> None:
        """Turn off a load with an optional transition time.

        Args:
            transition: The time in seconds to ramp the load down, defaults to immediate.
        """
        if transition is None:
            return await self.set_level(0)

        await self.ramp(LoadInterface.RampType.Fixed, transition, 0)

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
