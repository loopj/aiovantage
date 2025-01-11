"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface, method


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    # Properties
    value: Decimal | None = None

    # Methods
    @method("Temperature.GetValue", property="value")
    async def get_value(self) -> Decimal:
        """Get the value of a temperature sensor, using cached value if available.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValue
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        return await self.invoke("Temperature.GetValue")

    @method("Temperature.GetValueHW")
    async def get_value_hw(self) -> Decimal:
        """Get the value of a temperature sensor.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValueHW
        # -> R:INVOKE <id> <temp> Temperature.GetValueHW
        return await self.invoke("Temperature.GetValueHW")

    @method("Temperature.SetValue")
    async def set_value(self, value: Decimal) -> None:
        """Set the value of a temperature sensor.

        Args:
            value: The value to set the sensor to.
        """
        # INVOKE <id> Temperature.SetValue <value>
        # -> R:INVOKE <id> <rcode> Temperature.SetValue <value>
        await self.invoke("Temperature.SetValue", value)

    @method("Temperature.SetValueSW")
    async def set_value_sw(self, value: Decimal) -> None:
        """Set the cached value of a temperature sensor.

        Args:
            value: The value to set the sensor to.
        """
        # INVOKE <id> Temperature.SetValueSW <value>
        # -> R:INVOKE <id> <rcode> Temperature.SetValueSW <value>
        await self.invoke("Temperature.SetValueSW", value)
