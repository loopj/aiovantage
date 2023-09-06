"""Interface for querying and controlling thermostats."""

from decimal import Decimal
from enum import IntEnum
from typing import Union

from .base import Interface, InterfaceResponse, enum_result, fixed_result


class ThermostatInterface(Interface):
    """Interface for querying and controlling thermostats."""

    class OperationMode(IntEnum):
        """The operation mode of the thermostat."""

        OFF = 0
        COOL = 1
        HEAT = 2
        AUTO = 3
        UNKNOWN = 4

    class FanMode(IntEnum):
        """The fan mode of the thermostat."""

        OFF = 0
        ON = 1
        UNKNOWN = 2

    class DayMode(IntEnum):
        """The day mode of the thermostat."""

        DAY = 0
        NIGHT = 1
        UNKNOWN = 2
        STANDBY = 3

    class HoldMode(IntEnum):
        """The hold mode of the thermostat."""

        NORMAL = 0
        HOLD = 1
        UNKNOWN = 2

    class Status(IntEnum):
        """The status of the thermostat."""

        OFF = 0
        COOLING = 1
        HEATING = 2
        OFFLINE = 3

    async def get_indoor_temperature(self, vid: int) -> Decimal:
        """Get the current indoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The indoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetIndoorTemperature
        response = await self.invoke(vid, "Thermostat.GetIndoorTemperature")
        return self.parse_get_indoor_temperature_response(response)

    async def get_outdoor_temperature(self, vid: int) -> Decimal:
        """Get the current outdoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The outdoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetOutdoorTemperature
        response = await self.invoke(vid, "Thermostat.GetOutdoorTemperature")
        return self.parse_get_outdoor_temperature_response(response)

    async def get_heat_set_point(self, vid: int) -> Decimal:
        """Get the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The heat set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetHeatSetPoint
        response = await self.invoke(vid, "Thermostat.GetHeatSetPoint")
        return self.parse_get_heat_set_point_response(response)

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
        response = await self.invoke(vid, "Thermostat.GetCoolSetPoint")
        return self.parse_get_cool_set_point_response(response)

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
        response = await self.invoke(vid, "Thermostat.GetOperationMode")
        return self.parse_get_operation_mode_response(response)

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
        response = await self.invoke(vid, "Thermostat.GetFanMode")
        return self.parse_get_fan_mode_response(response)

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
        response = await self.invoke(vid, "Thermostat.GetDayMode")
        return self.parse_get_day_mode_response(response)

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
        response = await self.invoke(vid, "Thermostat.GetHoldMode")
        return self.parse_get_hold_mode_response(response)

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
        response = await self.invoke(vid, "Thermostat.GetStatus")
        return self.parse_get_status_response(response)

    async def get_auto_set_point(self, vid: int) -> Decimal:
        """Get the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The auto set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetAutoSetPoint
        response = await self.invoke(vid, "Thermostat.GetAutoSetPoint")
        return self.parse_get_auto_set_point_response(response)

    async def set_auto_set_point(self, vid: int, temp: Union[float, Decimal]) -> None:
        """Set the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The auto set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetAutoSetPoint", temp)

    @classmethod
    def parse_get_indoor_temperature_response(
        cls, response: InterfaceResponse
    ) -> Decimal:
        """Parse a 'Thermostat.GetIndoorTemperature' response."""
        # -> R:INVOKE <id> <temp> Thermostat.GetIndoorTemperature
        # -> S:STATUS <id> Thermostat.GetIndoorTemperature <temp>
        # -> EL: <id> Thermostat.GetIndoorTemperature <temp>
        return fixed_result(response)

    @classmethod
    def parse_get_outdoor_temperature_response(
        cls, response: InterfaceResponse
    ) -> Decimal:
        """Parse a 'Thermostat.GetOutdoorTemperature' response."""
        # -> R:INVOKE <id> <temp> Thermostat.GetOutdoorTemperature
        # -> S:STATUS <id> Thermostat.GetOutdoorTemperature <temp>
        # -> EL: <id> Thermostat.GetOutdoorTemperature <temp>
        return fixed_result(response)

    @classmethod
    def parse_get_heat_set_point_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Thermostat.GetHeatSetPoint' response."""
        # -> R:INVOKE <id> <temp> Thermostat.GetHeatSetPoint
        # -> S:STATUS <id> Thermostat.GetHeatSetPoint <temp>
        # -> EL: <id> Thermostat.GetHeatSetPoint <temp>
        return fixed_result(response)

    @classmethod
    def parse_get_cool_set_point_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Thermostat.GetCoolSetPoint' response."""
        # -> R:INVOKE <id> <temp> Thermostat.GetCoolSetPoint
        # -> S:STATUS <id> Thermostat.GetCoolSetPoint <temp>
        # -> EL: <id> Thermostat.GetCoolSetPoint <temp>
        return fixed_result(response)

    @classmethod
    def parse_get_operation_mode_response(
        cls, response: InterfaceResponse
    ) -> OperationMode:
        """Parse a 'Thermostat.GetOperationMode' response."""
        # -> R:INVOKE <id> <mode (Off|Cool|Heat|Auto|Unknown)> Thermostat.GetOperationMode
        # -> S:STATUS <id> Thermostat.GetOperationMode <mode (0/1/2/3/4)>
        # -> EL: <id> Thermostat.GetOperationMode <mode (0/1/2/3/4)>
        return enum_result(cls.OperationMode, response)

    @classmethod
    def parse_get_fan_mode_response(cls, response: InterfaceResponse) -> FanMode:
        """Parse a 'Thermostat.GetFanMode' response."""
        # -> R:INVOKE <id> <mode (Off|On|Unknown)> Thermostat.GetFanMode
        # -> S:STATUS <id> Thermostat.GetFanMode <mode (0/1/2)>
        # -> EL: <id> Thermostat.GetFanMode <mode (0/1/2)>
        return enum_result(cls.FanMode, response)

    @classmethod
    def parse_get_day_mode_response(cls, response: InterfaceResponse) -> DayMode:
        """Parse a 'Thermostat.GetDayMode' response."""
        # -> R:INVOKE <id> <mode (Day|Night|Unknown|Standby)> Thermostat.GetDayMode
        # -> S:STATUS <id> Thermostat.GetDayMode <mode (0/1/2/3)>
        # -> EL: <id> Thermostat.GetDayMode <mode (0/1/2/3)>
        return enum_result(cls.DayMode, response)

    @classmethod
    def parse_get_hold_mode_response(cls, response: InterfaceResponse) -> HoldMode:
        """Parse a 'Thermostat.GetHoldMode' response."""
        # -> R:INVOKE <id> <mode (Normal|Hold|Unknown)> Thermostat.GetHoldMode
        # -> S:STATUS <id> Thermostat.GetHoldMode <mode (0/1/2)>
        # -> EL: <id> Thermostat.GetHoldMode <mode (0/1/2)>
        return enum_result(cls.HoldMode, response)

    @classmethod
    def parse_get_status_response(cls, response: InterfaceResponse) -> Status:
        """Parse a 'Thermostat.GetStatus' response."""
        # -> R:INVOKE <id> <status (Off|Cooling|Heating|Offline)> Thermostat.GetStatus
        # -> S:STATUS <id> Thermostat.GetStatus <status (0/1/2/3)>
        # -> EL: <id> Thermostat.GetStatus <status (0/1/2/3)>
        return enum_result(cls.Status, response)

    @classmethod
    def parse_get_auto_set_point_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Thermostat.GetAutoSetPoint' response."""
        # -> R:INVOKE <id> <temp> Thermostat.GetAutoSetPoint
        # -> S:STATUS <id> Thermostat.GetAutoSetPoint <temp>
        # -> EL: <id> Thermostat.GetAutoSetPoint <temp>
        return fixed_result(response)
