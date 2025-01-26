"""Interface for querying and controlling power sensors."""

from decimal import Decimal

from .base import Interface


class PowerSensorInterface(Interface):
    """Interface for querying and controlling power sensors."""

    method_signatures = {
        "CurrentSensor.GetPower": Decimal,
        "CurrentSensor.GetPowerHW": Decimal,
    }

    async def get_power(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the value of a power sensor.

        Args:
            vid: The Vantage ID of the power sensor.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the power sensor, in Watts.
        """
        # INVOKE <id> PowerSensor.GetPower
        # -> R:INVOKE <id> <level> PowerSensor.GetPower
        return await self.invoke(
            vid, "PowerSensor.GetPowerHW" if hw else "PowerSensor.GetPower"
        )

    async def set_power(self, vid: int, value: Decimal, *, sw: bool = False) -> None:
        """Set the value of a power sensor.

        Args:
            vid: The Vantage ID of the power sensor.
            value: The value to set, in Watts.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> PowerSensor.SetPower <level>
        # -> R:INVOKE <id> <rcode> PowerSensor.SetPower <level>
        await self.invoke(
            vid, "PowerSensor.SetPowerSW" if sw else "PowerSensor.SetPower", value
        )
