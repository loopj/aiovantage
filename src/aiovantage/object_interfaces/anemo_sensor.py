"""Interface for querying and controlling anemo (wind) sensors."""

from decimal import Decimal

from .base import Interface, method


class AnemoSensorInterface(Interface):
    """Interface for querying and controlling anemo (wind) sensors."""

    # Properties
    speed: Decimal | None = None

    # Methods
    @method("AnemoSensor.GetSpeed", property="speed")
    async def get_speed(self) -> Decimal:
        """Get the speed of an anemo sensor, using cached value if available.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeed
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeed
        return await self.invoke("AnemoSensor.GetSpeed")

    @method("AnemoSensor.GetSpeedHW")
    async def get_speed_hw(self) -> Decimal:
        """Get the speed of an anemo sensor directly from the hardware.

        Returns:
            The speed of the anemo sensor, in mph.
        """
        # INVOKE <id> AnemoSensor.GetSpeedHW
        # -> R:INVOKE <id> <speed> AnemoSensor.GetSpeedHW
        return await self.invoke("AnemoSensor.GetSpeedHW")

    @method("AnemoSensor.SetSpeed")
    async def set_speed(self, speed: Decimal) -> None:
        """Set the speed of an anemo sensor.

        Args:
            speed: The speed to set, in mph.
        """
        # INVOKE <id> <rcode> AnemoSensor.SetSpeed <speed>
        # -> R:INVOKE <id> <rcode> AnemoSensor.SetSpeed <speed>
        await self.invoke("AnemoSensor.SetSpeed", speed)

    @method("AnemoSensor.SetSpeedSW")
    async def set_speed_sw(self, speed: Decimal) -> None:
        """Set the cached speed of an anemo sensor.

        Args:
            speed: The speed to set, in mph.
        """
        # INVOKE <id> <rcode> AnemoSensor.SetSpeedSW <speed>
        # -> R:INVOKE <id> <rcode> AnemoSensor.SetSpeedSW <speed>
        await self.invoke("AnemoSensor.SetSpeedSW", speed)
