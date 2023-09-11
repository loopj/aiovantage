"""Interface for querying and controlling thermostats."""

from decimal import Decimal
from enum import IntEnum
from typing import Union

from .base import Interface
from .parsers import parse_enum, parse_fixed


class ThermostatInterface(Interface):
    """Interface for querying and controlling thermostats."""

    response_parsers = {
        "Thermostat.GetIndoorTemperature": parse_fixed,
        "Thermostat.GetOutdoorTemperature": parse_fixed,
        "Thermostat.GetHeatSetPoint": parse_fixed,
        "Thermostat.GetCoolSetPoint": parse_fixed,
        "Thermostat.GetOperationMode": lambda r: parse_enum(
            ThermostatInterface.OperationMode, r
        ),
        "Thermostat.GetFanMode": lambda r: parse_enum(ThermostatInterface.FanMode, r),
        "Thermostat.GetDayMode": lambda r: parse_enum(ThermostatInterface.DayMode, r),
        "Thermostat.GetHoldMode": lambda r: parse_enum(ThermostatInterface.HoldMode, r),
        "Thermostat.GetStatus": lambda r: parse_enum(ThermostatInterface.Status, r),
        "Thermostat.GetAutoSetPoint": parse_fixed,
    }

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

    async def get_indoor_temperature(self, vid: int) -> Decimal:
        """Get the current indoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The indoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetIndoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetIndoorTemperature
        response = await self.invoke(vid, "Thermostat.GetIndoorTemperature")
        return ThermostatInterface.parse_response(response, Decimal)

    async def get_outdoor_temperature(self, vid: int) -> Decimal:
        """Get the current outdoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The outdoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetOutdoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetOutdoorTemperature
        response = await self.invoke(vid, "Thermostat.GetOutdoorTemperature")
        return ThermostatInterface.parse_response(response, Decimal)

    async def get_heat_set_point(self, vid: int) -> Decimal:
        """Get the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The heat set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetHeatSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetHeatSetPoint
        response = await self.invoke(vid, "Thermostat.GetHeatSetPoint")
        return ThermostatInterface.parse_response(response, Decimal)

    async def set_heat_set_point(self, vid: int, temp: Union[float, Decimal]) -> None:
        """Set the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The heat set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetHeatSetPoint", temp)

    async def get_cool_set_point(self, vid: int) -> Decimal:
        """Get the current cool set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The cool set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetCoolSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetCoolSetPoint
        response = await self.invoke(vid, "Thermostat.GetCoolSetPoint")
        return ThermostatInterface.parse_response(response, Decimal)

    async def set_cool_set_point(self, vid: int, temp: Union[float, Decimal]) -> None:
        """Set the current cool set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The cool set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetCoolSetPoint", temp)

    async def get_operation_mode(self, vid: int) -> OperationMode:
        """Get the current operation mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The operation mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetOperationMode
        # -> R:INVOKE <id> <mode (Off|Cool|Heat|Auto|Unknown)> Thermostat.GetOperationMode
        response = await self.invoke(vid, "Thermostat.GetOperationMode")
        return ThermostatInterface.parse_response(response, self.OperationMode)

    async def set_operation_mode(self, vid: int, mode: int) -> None:
        """Set the current operation mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The operation mode to set.
        """
        # INVOKE <id> Thermostat.SetOperationMode <mode>
        # -> R:INVOKE <id> Thermostat.SetOperationMode <mode>
        await self.invoke(vid, "Thermostat.SetOperationMode", mode)

    async def get_fan_mode(self, vid: int) -> FanMode:
        """Get the current fan mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The fan mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetFanMode
        # -> R:INVOKE <id> <mode (Off|On|Unknown)> Thermostat.GetFanMode
        response = await self.invoke(vid, "Thermostat.GetFanMode")
        return ThermostatInterface.parse_response(response, self.FanMode)

    async def set_fan_mode(self, vid: int, mode: int) -> None:
        """Set the current fan mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The fan mode to set.
        """
        # INVOKE <id> Thermostat.SetFanMode <mode>
        # -> R:INVOKE <id> Thermostat.SetFanMode <mode>
        await self.invoke(vid, "Thermostat.SetFanMode", mode)

    async def get_day_mode(self, vid: int) -> DayMode:
        """Get the current day mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The day mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetDayMode
        # -> R:INVOKE <id> <mode (Day|Night|Unknown|Standby)> Thermostat.GetDayMode
        response = await self.invoke(vid, "Thermostat.GetDayMode")
        return ThermostatInterface.parse_response(response, self.DayMode)

    async def set_day_mode(self, vid: int, mode: int) -> None:
        """Set the current day mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The day mode to set.
        """
        # INVOKE <id> Thermostat.SetDayMode <mode>
        # -> R:INVOKE <id> Thermostat.SetDayMode <mode>
        await self.invoke(vid, "Thermostat.SetDayMode", mode)

    async def get_hold_mode(self, vid: int) -> HoldMode:
        """Get the current hold mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The hold mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetHoldMode
        # -> R:INVOKE <id> <mode (Normal|Hold|Unknown)> Thermostat.GetHoldMode
        response = await self.invoke(vid, "Thermostat.GetHoldMode")
        return ThermostatInterface.parse_response(response, self.HoldMode)

    async def set_hold_mode(self, vid: int, mode: int) -> None:
        """Set the current hold mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The hold mode to set.
        """
        # INVOKE <id> Thermostat.SetHoldMode <mode>
        # -> R:INVOKE <id> Thermostat.SetHoldMode <mode>
        await self.invoke(vid, "Thermostat.SetHoldMode", mode)

    async def get_status(self, vid: int) -> Status:
        """Get the current status.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The status of the thermostat.
        """
        # INVOKE <id> Thermostat.GetStatus
        # -> R:INVOKE <id> <status (Off|Cooling|Heating|Offline)> Thermostat.GetStatus
        response = await self.invoke(vid, "Thermostat.GetStatus")
        return ThermostatInterface.parse_response(response, self.Status)

    async def get_auto_set_point(self, vid: int) -> Decimal:
        """Get the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The auto set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetAutoSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetAutoSetPoint
        response = await self.invoke(vid, "Thermostat.GetAutoSetPoint")
        return ThermostatInterface.parse_response(response, Decimal)

    async def set_auto_set_point(self, vid: int, temp: Union[float, Decimal]) -> None:
        """Set the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The auto set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetAutoSetPoint", temp)
