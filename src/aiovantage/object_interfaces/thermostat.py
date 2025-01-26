"""Interface for querying and controlling thermostats."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class ThermostatInterface(Interface):
    """Interface for querying and controlling thermostats."""

    class OperationMode(IntEnum):
        """Thermostat operation mode."""

        Off = 0
        Cool = 1
        Heat = 2
        Auto = 3
        Unknown = 4

    class FanMode(IntEnum):
        """Thermostat fan mode."""

        Off = 0
        On = 1
        Unknown = 2

    class DayMode(IntEnum):
        """Thermostat day mode."""

        Day = 0
        Night = 1
        Unknown = 2
        Standby = 3

    class HoldMode(IntEnum):
        """The hold mode of the thermostat."""

        Normal = 0
        Hold = 1
        Unknown = 2

    class Status(IntEnum):
        """The status of the thermostat."""

        Off = 0
        Cooling = 1
        Heating = 2
        Offline = 3

    method_signatures = {
        "Thermostat.GetIndoorTemperature": Decimal,
        "Thermostat.GetIndoorTemperatureHW": Decimal,
        "Thermostat.GetOutdoorTemperature": Decimal,
        "Thermostat.GetOutdoorTemperatureHW": Decimal,
        "Thermostat.GetHeatSetPoint": Decimal,
        "Thermostat.GetHeatSetPointHW": Decimal,
        "Thermostat.GetCoolSetPoint": Decimal,
        "Thermostat.GetCoolSetPointHW": Decimal,
        "Thermostat.GetOperationMode": OperationMode,
        "Thermostat.GetOperationModeHW": OperationMode,
        "Thermostat.GetFanMode": FanMode,
        "Thermostat.GetFanModeHW": FanMode,
        "Thermostat.GetDayMode": DayMode,
        "Thermostat.GetDayModeHW": DayMode,
        "Thermostat.GetHoldMode": HoldMode,
        "Thermostat.GetHoldModeHW": HoldMode,
        "Thermostat.GetStatus": Status,
        "Thermostat.GetStatusHW": Status,
        "Thermostat.GetAutoSetPoint": Decimal,
        "Thermostat.GetAutoSetPointHW": Decimal,
    }

    async def get_indoor_temperature(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the current indoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The indoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetIndoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetIndoorTemperature
        return await self.invoke(
            vid,
            "Thermostat.GetIndoorTemperatureHW"
            if hw
            else "Thermostat.GetIndoorTemperature",
        )

    async def set_indoor_temperature(self, vid: int, temp: float | Decimal) -> None:
        """Set the cached indoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The indoor temperature to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetIndoorTemperature <temp>
        # -> R:INVOKE <id> Thermostat.SetIndoorTemperature <temp>
        await self.invoke(vid, "Thermostat.SetIndoorTemperatureSW", temp)

    async def get_outdoor_temperature(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the current outdoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The outdoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetOutdoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetOutdoorTemperature
        return await self.invoke(
            vid,
            "Thermostat.GetOutdoorTemperatureHW"
            if hw
            else "Thermostat.GetOutdoorTemperature",
        )

    async def set_outdoor_temperature(self, vid: int, temp: float | Decimal) -> None:
        """Set the cached outdoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The outdoor temperature to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetOutdoorTemperature <temp>
        # -> R:INVOKE <id> Thermostat.SetOutdoorTemperature <temp>
        await self.invoke(vid, "Thermostat.SetOutdoorTemperatureSW", temp)

    async def get_heat_set_point(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The heat set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetHeatSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetHeatSetPoint
        return await self.invoke(
            vid, "Thermostat.GetHeatSetPointHW" if hw else "Thermostat.GetHeatSetPoint"
        )

    async def set_heat_set_point(
        self, vid: int, temp: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The heat set point to set, in degrees Celsius.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        await self.invoke(
            vid,
            "Thermostat.SetHeatSetPointSW" if sw else "Thermostat.SetHeatSetPoint",
            temp,
        )

    async def get_cool_set_point(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the current cool set point.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The cool set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetCoolSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetCoolSetPoint
        return await self.invoke(
            vid, "Thermostat.GetCoolSetPointHW" if hw else "Thermostat.GetCoolSetPoint"
        )

    async def set_cool_set_point(
        self, vid: int, temp: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the current cool set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The cool set point to set, in degrees Celsius.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        await self.invoke(
            vid,
            "Thermostat.SetCoolSetPointSW" if sw else "Thermostat.SetCoolSetPoint",
            temp,
        )

    async def get_operation_mode(self, vid: int, *, hw: bool = False) -> OperationMode:
        """Get the current operation mode.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The operation mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetOperationMode
        # -> R:INVOKE <id> <mode (Off|Cool|Heat|Auto|Unknown)> Thermostat.GetOperationMode
        return await self.invoke(
            vid,
            "Thermostat.GetOperationModeHW" if hw else "Thermostat.GetOperationMode",
        )

    async def set_operation_mode(
        self, vid: int, mode: int, *, sw: bool = False
    ) -> None:
        """Set the current operation mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The operation mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetOperationMode <mode>
        # -> R:INVOKE <id> Thermostat.SetOperationMode <mode>
        await self.invoke(
            vid,
            "Thermostat.SetOperationModeSW" if sw else "Thermostat.SetOperationMode",
            mode,
        )

    async def get_fan_mode(self, vid: int, *, hw: bool = False) -> FanMode:
        """Get the current fan mode.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The fan mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetFanMode
        # -> R:INVOKE <id> <mode (Off|On|Unknown)> Thermostat.GetFanMode
        return await self.invoke(
            vid, "Thermostat.GetFanModeHW" if hw else "Thermostat.GetFanMode"
        )

    async def set_fan_mode(self, vid: int, mode: int, *, sw: bool = False) -> None:
        """Set the current fan mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The fan mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetFanMode <mode>
        # -> R:INVOKE <id> Thermostat.SetFanMode <mode>
        await self.invoke(
            vid, "Thermostat.SetFanModeSW" if sw else "Thermostat.SetFanMode", mode
        )

    async def get_day_mode(self, vid: int, *, hw: bool = False) -> DayMode:
        """Get the current day mode.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The day mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetDayMode
        # -> R:INVOKE <id> <mode (Day|Night|Unknown|Standby)> Thermostat.GetDayMode
        return await self.invoke(
            vid, "Thermostat.GetDayModeHW" if hw else "Thermostat.GetDayMode"
        )

    async def set_day_mode(self, vid: int, mode: int, *, sw: bool = False) -> None:
        """Set the current day mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The day mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetDayMode <mode>
        # -> R:INVOKE <id> Thermostat.SetDayMode <mode>
        await self.invoke(
            vid, "Thermostat.SetDayModeSW" if sw else "Thermostat.SetDayMode", mode
        )

    async def set_hold_mode(self, vid: int, mode: int, *, sw: bool = False) -> None:
        """Set the current hold mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The hold mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetHoldMode <mode>
        # -> R:INVOKE <id> Thermostat.SetHoldMode <mode>
        await self.invoke(
            vid, "Thermostat.SetHoldModeSW" if sw else "Thermostat.SetHoldMode", mode
        )

    async def get_hold_mode(self, vid: int, *, hw: bool = False) -> HoldMode:
        """Get the current hold mode.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The hold mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetHoldMode
        # -> R:INVOKE <id> <mode (Normal|Hold|Unknown)> Thermostat.GetHoldMode
        return await self.invoke(
            vid, "Thermostat.GetHoldModeHW" if hw else "Thermostat.GetHoldMode"
        )

    async def get_status(self, vid: int, *, hw: bool = False) -> Status:
        """Get the current status.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The status of the thermostat.
        """
        # INVOKE <id> Thermostat.GetStatus
        # -> R:INVOKE <id> <status (Off|Cooling|Heating|Offline)> Thermostat.GetStatus
        return await self.invoke(
            vid, "Thermostat.GetStatusHW" if hw else "Thermostat.GetStatus"
        )

    async def set_status(self, vid: int, status: int) -> None:
        """Set the cached status.

        Args:
            vid: The Vantage ID of the thermostat.
            status: The status to set.
        """
        # INVOKE <id> Thermostat.SetStatusSW <status>
        # -> R:INVOKE <id> Thermostat.SetStatusSW <status>
        await self.invoke(vid, "Thermostat.SetStatusSW", status)

    async def get_auto_set_point(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The auto set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetAutoSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetAutoSetPoint
        return await self.invoke(
            vid, "Thermostat.GetAutoSetPointHW" if hw else "Thermostat.GetAutoSetPoint"
        )

    async def set_auto_set_point(
        self, vid: int, temp: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The auto set point to set, in degrees Celsius.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        await self.invoke(
            vid,
            "Thermostat.SetAutoSetPointSW" if sw else "Thermostat.SetAutoSetPoint",
            temp,
        )
