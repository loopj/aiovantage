"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal

from .base import Interface


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    method_signatures = {
        "AnemoSensor.GetSpeed": Decimal,
        "AnemoSensor.GetSpeedHW": Decimal,
    }

    async def get_speed(self, vid: int) -> Decimal:
        """Get the speed of an anemo sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the anemo sensor.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        return await self.invoke(vid, "AnemoSensor.GetSpeed", as_type=Decimal)

    async def get_speed_hw(self, vid: int) -> Decimal:
        """Get the speed of an anemo sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the anemo sensor.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeedHW
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeedHW
        return await self.invoke(vid, "AnemoSensor.GetSpeedHW", as_type=Decimal)
