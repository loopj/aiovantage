"""Interface for querying and controlling sensors."""

from decimal import Decimal
from typing import Sequence

from .base import Interface


class TemperatureInterface(Interface):
    """Interface for querying and controlling sensors."""

    async def get_value(self, vid: int) -> Decimal:
        """Get the value of a temperature sensor.

        Args:
            vid: The Vantage ID of the temperature sensor.
        """
        # INVOKE <id> Temperature.GetValue
        # -> R:INVOKE <id> <temp> Temperature.GetValue
        response = await self.invoke(vid, "Temperature.GetValue")
        level = Decimal(response.args[1])

        return level

    @classmethod
    def parse_get_value_status(cls, args: Sequence[str]) -> Decimal:
        """Parse a 'Temperature.GetValue' event.

        Args:
            args: The arguments of the event.

        Returns:
            The level of the sensor.
        """
        # ELLOG STATUS ON
        # -> EL: <id> Temperature.GetValue <temp>

        # STATUS ADD <id>
        # -> S:STATUS <id> Temperature.GetValue <temp>
        return Decimal(args[0]) / 1000
