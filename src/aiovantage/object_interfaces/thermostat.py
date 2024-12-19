"""Interface for querying and controlling thermostats."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class ThermostatInterface(Interface):
    """Interface for querying and controlling thermostats."""

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

    method_signatures = {
        "Thermostat.GetIndoorTemperature": Decimal,
        "Thermostat.GetOutdoorTemperature": Decimal,
        "Thermostat.GetHeatSetPoint": Decimal,
        "Thermostat.GetCoolSetPoint": Decimal,
        "Thermostat.GetOperationMode": OperationMode,
        "Thermostat.GetFanMode": FanMode,
        "Thermostat.GetDayMode": DayMode,
        "Thermostat.GetHoldMode": HoldMode,
        "Thermostat.GetStatus": Status,
        "Thermostat.GetAutoSetPoint": Decimal,
    }

    # Properties
    indoor_temperature: Decimal | None = None
    heat_set_point: Decimal | None = None
    cool_set_point: Decimal | None = None
    auto_set_point: Decimal | None = None
    operation_mode: OperationMode | None = OperationMode.Unknown
    fan_mode: FanMode | None = FanMode.Unknown
    status: Status | None = Status.Offline  # Not available in 2.x firmware
    outdoor_temperature: Decimal | None = None
    hold_mode: HoldMode | None = None  # Not part of the interface, just for convenience
    day_mode: DayMode | None = None  # Not part of the interface, just for convenience

    # Methods
    async def get_indoor_temperature(self) -> Decimal:
        """Get the current indoor temperature.

        Returns:
            The indoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetIndoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetIndoorTemperature
        return await self.invoke("Thermostat.GetIndoorTemperature", as_type=Decimal)

    async def get_outdoor_temperature(self) -> Decimal:
        """Get the current outdoor temperature.

        Returns:
            The outdoor temperature of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetOutdoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetOutdoorTemperature
        return await self.invoke("Thermostat.GetOutdoorTemperature", as_type=Decimal)

    async def get_heat_set_point(self) -> Decimal:
        """Get the current heat set point.

        Returns:
            The heat set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetHeatSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetHeatSetPoint
        return await self.invoke("Thermostat.GetHeatSetPoint", as_type=Decimal)

    async def set_heat_set_point(self, temp: float | Decimal) -> None:
        """Set the current heat set point.

        Args:
            temp: The heat set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        await self.invoke("Thermostat.SetHeatSetPoint", temp)

    async def get_cool_set_point(self) -> Decimal:
        """Get the current cool set point.

        Returns:
            The cool set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetCoolSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetCoolSetPoint
        return await self.invoke("Thermostat.GetCoolSetPoint", as_type=Decimal)

    async def set_cool_set_point(self, temp: float | Decimal) -> None:
        """Set the current cool set point.

        Args:
            temp: The cool set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        await self.invoke("Thermostat.SetCoolSetPoint", temp)

    async def get_operation_mode(self) -> OperationMode:
        """Get the current operation mode.

        Returns:
            The operation mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetOperationMode
        # -> R:INVOKE <id> <mode (Off|Cool|Heat|Auto|Unknown)> Thermostat.GetOperationMode
        return await self.invoke(
            "Thermostat.GetOperationMode", as_type=ThermostatInterface.OperationMode
        )

    async def set_operation_mode(self, mode: int) -> None:
        """Set the current operation mode.

        Args:
            mode: The operation mode to set.
        """
        # INVOKE <id> Thermostat.SetOperationMode <mode>
        # -> R:INVOKE <id> Thermostat.SetOperationMode <mode>
        await self.invoke("Thermostat.SetOperationMode", mode)

    async def get_fan_mode(self) -> FanMode:
        """Get the current fan mode.

        Returns:
            The fan mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetFanMode
        # -> R:INVOKE <id> <mode (Off|On|Unknown)> Thermostat.GetFanMode
        return await self.invoke(
            "Thermostat.GetFanMode", as_type=ThermostatInterface.FanMode
        )

    async def set_fan_mode(self, mode: int) -> None:
        """Set the current fan mode.

        Args:
            mode: The fan mode to set.
        """
        # INVOKE <id> Thermostat.SetFanMode <mode>
        # -> R:INVOKE <id> Thermostat.SetFanMode <mode>
        await self.invoke("Thermostat.SetFanMode", mode)

    async def get_day_mode(self) -> DayMode:
        """Get the current day mode.

        Returns:
            The day mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetDayMode
        # -> R:INVOKE <id> <mode (Day|Night|Unknown|Standby)> Thermostat.GetDayMode
        return await self.invoke(
            "Thermostat.GetDayMode", as_type=ThermostatInterface.DayMode
        )

    async def set_day_mode(self, mode: int) -> None:
        """Set the current day mode.

        Args:
            mode: The day mode to set.
        """
        # INVOKE <id> Thermostat.SetDayMode <mode>
        # -> R:INVOKE <id> Thermostat.SetDayMode <mode>
        await self.invoke("Thermostat.SetDayMode", mode)

    async def get_hold_mode(self) -> HoldMode:
        """Get the current hold mode.

        Returns:
            The hold mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetHoldMode
        # -> R:INVOKE <id> <mode (Normal|Hold|Unknown)> Thermostat.GetHoldMode
        return await self.invoke(
            "Thermostat.GetHoldMode", as_type=ThermostatInterface.HoldMode
        )

    async def set_hold_mode(self, mode: int) -> None:
        """Set the current hold mode.

        Args:
            mode: The hold mode to set.
        """
        # INVOKE <id> Thermostat.SetHoldMode <mode>
        # -> R:INVOKE <id> Thermostat.SetHoldMode <mode>
        await self.invoke("Thermostat.SetHoldMode", mode)

    async def get_status(self) -> Status:
        """Get the current status.

        Returns:
            The status of the thermostat.
        """
        # INVOKE <id> Thermostat.GetStatus
        # -> R:INVOKE <id> <status (Off|Cooling|Heating|Offline)> Thermostat.GetStatus
        return await self.invoke(
            "Thermostat.GetStatus", as_type=ThermostatInterface.Status
        )

    async def get_auto_set_point(self) -> Decimal:
        """Get the current auto set point.

        Returns:
            The auto set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetAutoSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetAutoSetPoint
        return await self.invoke("Thermostat.GetAutoSetPoint", as_type=Decimal)

    async def set_auto_set_point(self, temp: float | Decimal) -> None:
        """Set the current auto set point.

        Args:
            temp: The auto set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        await self.invoke("Thermostat.SetAutoSetPoint", temp)
