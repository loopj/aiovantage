"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Temperature.GetValue": Decimal,
        "Temperature.GetValueHW": Decimal,
    }

    # Properties
    value: Decimal | None = None

    # Methods
    async def get_value(self) -> Decimal:
        """Get the value of a temperature sensor, using cached value if available.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValue
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        return await self.invoke("Temperature.GetValue", as_type=Decimal)

    async def get_value_hw(self) -> Decimal:
        """Get the value of a temperature sensor.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValueHW
        # -> R:INVOKE <id> <temp> Temperature.GetValueHW
        return await self.invoke("Temperature.GetValueHW", as_type=Decimal)

    async def set_value(self, value: Decimal) -> None:
        """Set the value of a temperature sensor.

        Args:
            value: The value to set the sensor to.
        """
        # INVOKE <id> Temperature.SetValue <value>
        # -> R:INVOKE <id> <rcode> Temperature.SetValue <value>
        await self.invoke("Temperature.SetValue", value)

    async def set_value_sw(self, value: Decimal) -> None:
        """Set the cached value of a temperature sensor.

        Args:
            value: The value to set the sensor to.
        """
        # INVOKE <id> Temperature.SetValueSW <value>
        # -> R:INVOKE <id> <rcode> Temperature.SetValueSW <value>
        await self.invoke("Temperature.SetValueSW", value)
