"""Interface for querying and controlling thermostats."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface, method


class ThermostatInterface(Interface):
    """Interface for querying and controlling thermostats."""

    # Types
    class OperationMode(IntEnum):
        """The operation mode of the thermostat."""

        Off = 0
        Cool = 1
        Heat = 2
        Auto = 3
        Unknown = 4

    class FanMode(IntEnum):
        """The fan mode of the thermostat."""

        Off = 0
        On = 1
        Unknown = 2

    class DayMode(IntEnum):
        """The day mode of the thermostat."""

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

    # Properties
    indoor_temperature: Decimal | None = None
    heat_set_point: Decimal | None = None
    cool_set_point: Decimal | None = None
    auto_set_point: Decimal | None = None
    operation_mode: OperationMode | None = OperationMode.Unknown
    fan_mode: FanMode | None = FanMode.Unknown
    status: Status | None = Status.Offline
    outdoor_temperature: Decimal | None = None

    # Methods
    @method("Thermostat.GetIndoorTemperature", property="indoor_temperature")
    @method("Thermostat.GetIndoorTemperatureHW")
    async def get_indoor_temperature(self, *, hw: bool = False) -> Decimal:
        """Get the current indoor temperature.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The indoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetIndoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetIndoorTemperature
        return await self.invoke(
            "Thermostat.GetIndoorTemperatureHW"
            if hw
            else "Thermostat.GetIndoorTemperature"
        )

    @method("Thermostat.SetIndoorTemperatureSW")
    async def set_indoor_temperature(self, temp: float | Decimal) -> None:
        """Set the cached indoor temperature.

        Args:
            temp: The indoor temperature to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetIndoorTemperature <temp>
        # -> R:INVOKE <id> Thermostat.SetIndoorTemperature <temp>
        await self.invoke("Thermostat.SetIndoorTemperatureSW", temp)

    @method("Thermostat.GetOutdoorTemperature", property="outdoor_temperature")
    @method("Thermostat.GetOutdoorTemperatureHW")
    async def get_outdoor_temperature(self, *, hw: bool = False) -> Decimal:
        """Get the current outdoor temperature.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The outdoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetOutdoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetOutdoorTemperature
        return await self.invoke(
            "Thermostat.GetOutdoorTemperatureHW"
            if hw
            else "Thermostat.GetOutdoorTemperature"
        )

    @method("Thermostat.SetOutdoorTemperatureSW")
    async def set_outdoor_temperature(self, temp: float | Decimal) -> None:
        """Set the cached outdoor temperature.

        Args:
            temp: The outdoor temperature to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetOutdoorTemperature <temp>
        # -> R:INVOKE <id> Thermostat.SetOutdoorTemperature <temp>
        await self.invoke("Thermostat.SetOutdoorTemperatureSW", temp)

    @method("Thermostat.GetHeatSetPoint", property="heat_set_point")
    @method("Thermostat.GetHeatSetPointHW")
    async def get_heat_set_point(self, *, hw: bool = False) -> Decimal:
        """Get the current heat set point.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The heat set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetHeatSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetHeatSetPoint
        return await self.invoke(
            "Thermostat.GetHeatSetPointHW" if hw else "Thermostat.GetHeatSetPoint"
        )

    @method("Thermostat.SetHeatSetPoint")
    @method("Thermostat.SetHeatSetPointSW")
    async def set_heat_set_point(
        self, temp: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the current heat set point.

        Args:
            temp: The heat set point to set, in degrees Celsius.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        await self.invoke(
            "Thermostat.SetHeatSetPointSW" if sw else "Thermostat.SetHeatSetPoint", temp
        )

    @method("Thermostat.GetCoolSetPoint", property="cool_set_point")
    @method("Thermostat.GetCoolSetPointHW")
    async def get_cool_set_point(self, *, hw: bool = False) -> Decimal:
        """Get the current cool set point.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The cool set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetCoolSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetCoolSetPoint
        return await self.invoke(
            "Thermostat.GetCoolSetPointHW" if hw else "Thermostat.GetCoolSetPoint"
        )

    @method("Thermostat.SetCoolSetPoint")
    @method("Thermostat.SetCoolSetPointSW")
    async def set_cool_set_point(
        self, temp: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the current cool set point.

        Args:
            temp: The cool set point to set, in degrees Celsius.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        await self.invoke(
            "Thermostat.SetCoolSetPointSW" if sw else "Thermostat.SetCoolSetPoint", temp
        )

    @method("Thermostat.GetOperationMode", property="operation_mode")
    @method("Thermostat.GetOperationModeHW")
    async def get_operation_mode(self, *, hw: bool = False) -> OperationMode:
        """Get the current operation mode.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The operation mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetOperationMode
        # -> R:INVOKE <id> <mode (Off|Cool|Heat|Auto|Unknown)> Thermostat.GetOperationMode
        return await self.invoke(
            "Thermostat.GetOperationModeHW" if hw else "Thermostat.GetOperationMode"
        )

    @method("Thermostat.SetOperationMode")
    @method("Thermostat.SetOperationModeSW")
    async def set_operation_mode(self, mode: int, *, sw: bool = False) -> None:
        """Set the current operation mode.

        Args:
            mode: The operation mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetOperationMode <mode>
        # -> R:INVOKE <id> Thermostat.SetOperationMode <mode>
        await self.invoke(
            "Thermostat.SetOperationModeSW" if sw else "Thermostat.SetOperationMode",
            mode,
        )

    @method("Thermostat.GetFanMode", property="fan_mode")
    @method("Thermostat.GetFanModeHW")
    async def get_fan_mode(self, *, hw: bool = False) -> FanMode:
        """Get the current fan mode.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The fan mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetFanMode
        # -> R:INVOKE <id> <mode (Off|On|Unknown)> Thermostat.GetFanMode
        return await self.invoke(
            "Thermostat.GetFanModeHW" if hw else "Thermostat.GetFanMode"
        )

    @method("Thermostat.SetFanMode")
    @method("Thermostat.SetFanModeSW")
    async def set_fan_mode(self, mode: int, *, sw: bool = False) -> None:
        """Set the current fan mode.

        Args:
            mode: The fan mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetFanMode <mode>
        # -> R:INVOKE <id> Thermostat.SetFanMode <mode>
        await self.invoke(
            "Thermostat.SetFanModeSW" if sw else "Thermostat.SetFanMode", mode
        )

    @method("Thermostat.GetDayMode")
    @method("Thermostat.GetDayModeHW")
    async def get_day_mode(self, *, hw: bool = False) -> DayMode:
        """Get the current day mode.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The day mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetDayMode
        # -> R:INVOKE <id> <mode (Day|Night|Unknown|Standby)> Thermostat.GetDayMode
        return await self.invoke(
            "Thermostat.GetDayModeHW" if hw else "Thermostat.GetDayMode"
        )

    @method("Thermostat.SetDayMode")
    @method("Thermostat.SetDayModeSW")
    async def set_day_mode(self, mode: int, *, sw: bool = False) -> None:
        """Set the current day mode.

        Args:
            mode: The day mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetDayMode <mode>
        # -> R:INVOKE <id> Thermostat.SetDayMode <mode>
        await self.invoke(
            "Thermostat.SetDayModeSW" if sw else "Thermostat.SetDayMode", mode
        )

    @method("Thermostat.SetHoldMode")
    @method("Thermostat.SetHoldModeSW")
    async def set_hold_mode(self, mode: int, *, sw: bool = False) -> None:
        """Set the current hold mode.

        Args:
            mode: The hold mode to set.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetHoldMode <mode>
        # -> R:INVOKE <id> Thermostat.SetHoldMode <mode>
        await self.invoke(
            "Thermostat.SetHoldModeSW" if sw else "Thermostat.SetHoldMode", mode
        )

    @method("Thermostat.GetHoldMode")
    @method("Thermostat.GetHoldModeHW")
    async def get_hold_mode(self, *, hw: bool = False) -> HoldMode:
        """Get the current hold mode.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The hold mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetHoldMode
        # -> R:INVOKE <id> <mode (Normal|Hold|Unknown)> Thermostat.GetHoldMode
        return await self.invoke(
            "Thermostat.GetHoldModeHW" if hw else "Thermostat.GetHoldMode"
        )

    @method("Thermostat.GetStatus", property="status")
    @method("Thermostat.GetStatusHW")
    async def get_status(self, *, hw: bool = False) -> Status:
        """Get the current status.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The status of the thermostat.
        """
        # INVOKE <id> Thermostat.GetStatus
        # -> R:INVOKE <id> <status (Off|Cooling|Heating|Offline)> Thermostat.GetStatus
        return await self.invoke(
            "Thermostat.GetStatusHW" if hw else "Thermostat.GetStatus"
        )

    @method("Thermostat.SetStatusSW")
    async def set_status(self, status: int) -> None:
        """Set the cached status.

        Args:
            status: The status to set.
        """
        # INVOKE <id> Thermostat.SetStatusSW <status>
        # -> R:INVOKE <id> Thermostat.SetStatusSW <status>
        await self.invoke("Thermostat.SetStatusSW", status)

    @method("Thermostat.GetAutoSetPoint", property="auto_set_point")
    @method("Thermostat.GetAutoSetPointHW")
    async def get_auto_set_point(self, *, hw: bool = False) -> Decimal:
        """Get the current auto set point.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The auto set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetAutoSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetAutoSetPoint
        return await self.invoke(
            "Thermostat.GetAutoSetPointHW" if hw else "Thermostat.GetAutoSetPoint"
        )

    @method("Thermostat.SetAutoSetPoint")
    @method("Thermostat.SetAutoSetPointSW")
    async def set_auto_set_point(
        self, temp: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the current auto set point.

        Args:
            temp: The auto set point to set, in degrees Celsius.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        await self.invoke(
            "Thermostat.SetAutoSetPointSW" if sw else "Thermostat.SetAutoSetPoint", temp
        )
