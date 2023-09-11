"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal
from typing import Sequence

from .base import Interface


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    async def get_speed(self, vid: int) -> Decimal:
        """Get the value of an anemo sensor, using a cached value if available.

        Args:
            vid: The Vantage ID of the anemo sensor.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        response = await self.invoke(vid, "AnemoSensor.GetSpeed")

        # Older firmware response in thousandths of a mph, newer as fixed point
        level = Decimal(response.args[1].replace(".", "")) / 1000

        return level

    async def get_speed_hw(self, vid: int) -> Decimal:
        """Get the value of an anemo sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the anemo sensor.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeedHW
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeedHW
        response = await self.invoke(vid, "AnemoSensor.GetSpeedHW")

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
