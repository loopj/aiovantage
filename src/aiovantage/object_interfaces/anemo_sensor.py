"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal

from .base import Interface


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    method_signatures = {
        "AnemoSensor.GetSpeed": Decimal,
        "AnemoSensor.GetSpeedHW": Decimal,
    }

    speed: Decimal | None = None

    async def get_speed(self) -> Decimal:
        """Get the speed of an anemo sensor, using cached value if available.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        return await self.invoke("AnemoSensor.GetSpeed", as_type=Decimal)

    async def get_speed_hw(self) -> Decimal:
        """Get the speed of an anemo sensor directly from the hardware.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeedHW
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeedHW
        return await self.invoke("AnemoSensor.GetSpeedHW", as_type=Decimal)
