"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal

from .base import Interface


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    method_signatures = {
        "AnemoSensor.GetSpeed": Decimal,
        "AnemoSensor.GetSpeedHW": Decimal,
    }

    async def get_speed(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the speed of an anemo sensor.

        Args:
            vid: The ID of the sensor.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        return await self.invoke(
            vid, "AnemoSensor.GetSpeedHW" if hw else "AnemoSensor.GetSpeed"
        )

    async def set_speed(self, vid: int, speed: Decimal, *, sw: bool = False) -> None:
        """Set the speed of an anemo sensor.

        Args:
            vid: The ID of the sensor.
            speed: The speed to set, in mph.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> AnemoSensor.SetSpeed <speed>
        # -> R:INVOKE <id> <rcode> AnemoSensor.SetSpeed <speed>
        await self.invoke(
            vid, "AnemoSensor.SetSpeedSW" if sw else "AnemoSensor.SetSpeed", speed
        )
