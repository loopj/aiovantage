"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface
from .parsers import parse_fixed


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    response_parsers = {
        "Temperature.GetValue": parse_fixed,
        "Temperature.GetValueHW": parse_fixed,
    }

    async def get_value(self, vid: int) -> Decimal:
        """Get the value of a temperature sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the temperature sensor.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValue
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        response = await self.invoke(vid, "Temperature.GetValue")
        return TemperatureInterface.parse_response(response, Decimal)

    async def get_value_hw(self, vid: int) -> Decimal:
        """Get the value of a temperature sensor.

        Args:
            vid: The Vantage ID of the temperature sensor.

        Returns:
            The value of the temperature sensor, in degrees Celsius.
        """
        # INVOKE <id> Temperature.GetValueHW
        # -> R:INVOKE <id> <temp> Temperature.GetValueHW
        response = await self.invoke(vid, "Temperature.GetValueHW")
        return TemperatureInterface.parse_response(response, Decimal)
