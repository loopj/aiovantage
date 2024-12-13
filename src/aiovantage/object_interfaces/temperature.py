"""Interface for querying and controlling sensors."""

from decimal import Decimal

from aiovantage.object_interfaces.base import Interface


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Temperature.GetValue": Decimal,
        "Temperature.GetValueHW": Decimal,
    }

    value: Decimal

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
