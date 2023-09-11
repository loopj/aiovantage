"""Interface for querying and controlling light sensors."""

from decimal import Decimal
from typing import Sequence

from .base import Interface


class LightSensorInterface(Interface):
    """Interface for querying and controlling light sensors."""

    async def get_level(self, vid: int) -> Decimal:
        """Get the level of a light sensor, using a cached value if available.

        Args:
            vid: The Vantage ID of the light sensor.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevel
        # -> R:INVOKE <id> <level> LightSensor.GetLevel
        response = await self.invoke(vid, "LightSensor.GetLevel")

        # Older firmware response in thousandths of a foot-candle, newer as fixed point
        level = Decimal(response.args[1].replace(".", "")) / 1000

        return level

    async def get_level_hw(self, vid: int) -> Decimal:
        """Get the level of a light sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the light sensor.

        Returns:
            The level of the light sensor, in foot-candles.
        """
        # INVOKE <id> LightSensor.GetLevelHW
        # -> R:INVOKE <id> <level> LightSensor.GetLevelHW
        response = await self.invoke(vid, "LightSensor.GetLevelHW")

        # Older firmware response in thousandths of a foot-candle, newer as fixed point
        level = Decimal(response.args[1].replace(".", "")) / 1000

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
