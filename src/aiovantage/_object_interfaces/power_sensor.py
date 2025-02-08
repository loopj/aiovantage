from decimal import Decimal

from typing_extensions import override

from .base import Interface, method


class PowerSensorInterface(Interface):
    """Power sensor interface."""

    interface_name = "PowerSensor"

    # Properties
    power: Decimal | None = None

    # Methods
    @method("GetPower", "GetPowerHW", property="power")
    async def get_power(self, *, hw: bool = False) -> Decimal:
        """Get the value of a power sensor.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the power sensor, in Watts.
        """
        # INVOKE <id> PowerSensor.GetPower
        # -> R:INVOKE <id> <level> PowerSensor.GetPower
        return await self.invoke(
            "PowerSensor.GetPowerHW" if hw else "PowerSensor.GetPower"
        )

    @method("SetPower", "SetPowerSW")
    async def set_power(self, value: Decimal, *, sw: bool = False) -> None:
        """Set the value of a power sensor.

        Args:
            value: The value to set, in Watts.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> PowerSensor.SetPower <level>
        # -> R:INVOKE <id> <rcode> PowerSensor.SetPower <level>
        await self.invoke(
            "PowerSensor.SetPowerSW" if sw else "PowerSensor.SetPower", value
        )

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "POWER":
            # STATUS POWER
            # -> S:POWER <id> <power>
            return self.update_properties({"power": Decimal(args[0])})

        return super().handle_category_status(category, *args)
