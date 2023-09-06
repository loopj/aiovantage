"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface, InterfaceResponse, fixed_result


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    async def get_value(self, vid: int) -> Decimal:
        """Get the value of a temperature sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the temperature sensor.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValue
        response = await self.invoke(vid, "Temperature.GetValue")
        return self.parse_get_value_response(response)

    async def get_value_hw(self, vid: int) -> Decimal:
        """Get the value of a temperature sensor.

        Args:
            vid: The Vantage ID of the temperature sensor.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValueHW
        response = await self.invoke(vid, "Temperature.GetValueHW")
        return self.parse_get_value_response(response)

    @classmethod
    def parse_get_value_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Temperature.GetValue' response."""
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        # -> S:STATUS <id> Temperature.GetValue <temp>
        # -> EL: <id> Temperature.GetValue <temp>
        return fixed_result(response)
