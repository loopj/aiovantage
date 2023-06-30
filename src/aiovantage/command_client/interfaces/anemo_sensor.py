"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal
from typing import Sequence

from .base import Interface


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    async def get_speed(self, vid: int) -> Decimal:
        """Get the value of an anemo sensor, in mph.

        Args:
            vid: The Vantage ID of the anemo sensor.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        response = await self.invoke(vid, "AnemoSensor.GetSpeed")
        level = Decimal(response.args[1])

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
