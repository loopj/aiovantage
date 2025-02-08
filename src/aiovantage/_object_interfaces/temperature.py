from decimal import Decimal

from typing_extensions import override

from .base import Interface, method


class TemperatureInterface(Interface):
    """Temperature interface."""

    interface_name = "Temperature"

    # Properties
    value: Decimal | None = None

    # Methods
    @method("GetValue", "GetValueHW", property="value")
    async def get_value(self, *, hw: bool = False) -> Decimal:
        """Get the value of a temperature sensor.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValue
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        return await self.invoke(
            "Temperature.GetValueHW" if hw else "Temperature.GetValue"
        )

    @method("SetValue", "SetValueSW")
    async def set_value(self, value: Decimal, *, sw: bool = False) -> None:
        """Set the value of a temperature sensor.

        Args:
            value: The value to set the sensor to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Temperature.SetValue <value>
        # -> R:INVOKE <id> <rcode> Temperature.SetValue <value>
        await self.invoke(
            "Temperature.SetValueSW" if sw else "Temperature.SetValue", value
        )

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "TEMP":
            # STATUS TEMP
            # -> S:TEMP <id> <temp>
            return self.update_properties({"value": Decimal(args[0])})

        return super().handle_category_status(category, *args)
