"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Temperature.GetValue": Decimal,
        "Temperature.GetValueHW": Decimal,
    }

    async def get_value(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the value of a temperature sensor.

        Args:
            vid: The Vantage ID of the temperature object.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValue
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        return await self.invoke(
            vid, "Temperature.GetValueHW" if hw else "Temperature.GetValue"
        )

    async def set_value(self, vid: int, value: Decimal, *, sw: bool = False) -> None:
        """Set the value of a temperature sensor.

        Args:
            vid: The Vantage ID of the temperature object.
            value: The value to set the sensor to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Temperature.SetValue <value>
        # -> R:INVOKE <id> <rcode> Temperature.SetValue <value>
        await self.invoke(
            vid, "Temperature.SetValueSW" if sw else "Temperature.SetValue", value
        )
