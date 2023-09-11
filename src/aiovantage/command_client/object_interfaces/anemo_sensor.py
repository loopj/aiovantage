"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal

from .base import Interface, InterfaceResponse, fixed_result


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    async def get_speed(self, vid: int) -> Decimal:
        """Get the speed of an anemo sensor, using cached value if available.

        Args:
            vid: The Vantage ID of the anemo sensor.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        response = await self.invoke(vid, "AnemoSensor.GetSpeed")
        return self.parse_get_speed_response(response)

    async def get_speed_hw(self, vid: int) -> Decimal:
        """Get the speed of an anemo sensor directly from the hardware.

        Args:
            vid: The Vantage ID of the anemo sensor.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeedHW
        response = await self.invoke(vid, "AnemoSensor.GetSpeedHW")
        return self.parse_get_speed_response(response)

    @classmethod
    def parse_get_speed_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'AnemoSensor.GetSpeed' response."""
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        # -> S:STATUS <id> AnemoSensor.GetSpeed <speed>
        # -> EL: <id> AnemoSensor.GetSpeed <speed>
        return fixed_result(response)
