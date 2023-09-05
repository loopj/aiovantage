"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal
from typing import Sequence

from .base import Interface


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    async def get_speed(self, vid: int, cached: bool = False) -> Decimal:
        """Get the value of an anemo sensor, in mph.

        Args:
            vid: The Vantage ID of the anemo sensor.
            cached: Whether to use the cached value or fetch a new one.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        method = "AnemoSensor.GetSpeed" if cached else "AnemoSensor.GetSpeedHW"
        response = await self.invoke(vid, method)

        # Older firmware response in thousandths of a mph, newer as fixed point
        level = Decimal(response.args[1].replace(".", "")) / 1000

        return level

    @classmethod
    def parse_get_speed_status(cls, args: Sequence[str]) -> Decimal:
        """Parse a 'AnemoSensor.GetSpeed' event.

        Args:
            args: The arguments of the event.

        Returns:
            The value of the anemo sensor, in mph.
        """
        # ELLOG STATUS ON
        # -> EL: <id> AnemoSensor.GetSpeed <speed>
        # STATUS ADD <id>
        # -> S:STATUS <id> AnemoSensor.GetSpeed <speed>
        return Decimal(args[0]) / 1000
