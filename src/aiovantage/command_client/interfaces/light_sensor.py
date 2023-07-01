"""Interface for querying and controlling light sensors."""

from decimal import Decimal
from typing import Sequence

from .base import Interface


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    async def get_level(self, vid: int) -> Decimal:
        """Get the level of a light sensor, in foot-candles.

        Args:
            vid: The Vantage ID of the light sensor.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        response = await self.invoke(vid, "LightSensor.GetLevel")
        level = Decimal(response.args[1])

        return level

    @classmethod
    def parse_get_level_status(cls, args: Sequence[str]) -> Decimal:
        """Parse a 'LightSensor.GetLevel' event.

        Args:
            args: The arguments of the event.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # ELLOG STATUS ON
        # -> EL: <id> LightSensor.GetLevel <level>
        # STATUS ADD <id>
        # -> S:STATUS <id> LightSensor.GetLevel <level>
        return Decimal(args[0]) / 1000
