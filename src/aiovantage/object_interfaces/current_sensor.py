"""Interface for querying and controlling current sensors."""

from decimal import Decimal

from .base import Interface


class CurrentSensorInterface(Interface):
    """Interface for querying and controlling current sensors."""

    method_signatures = {
        "CurrentSensor.GetCurrent": Decimal,
        "CurrentSensor.GetCurrentHW": Decimal,
    }

    async def get_current(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the value of a current sensor.

        Args:
            vid: The Vantage ID of the current sensor.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the current sensor, in Amps.
        """
        # INVOKE <id> CurrentSensor.GetCurrent
        # -> R:INVOKE <id> <level> CurrentSensor.GetCurrent
        return await self.invoke(
            vid, "CurrentSensor.GetCurrentHW" if hw else "CurrentSensor.GetCurrent"
        )

    async def set_current(self, vid: int, value: Decimal, *, sw: bool = False) -> None:
        """Set the value of a current sensor.

        Args:
            vid: The Vantage ID of the current sensor.
            value: The value to set, in Amps.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> CurrentSensor.SetCurrent <level>
        # -> R:INVOKE <id> <rcode> CurrentSensor.SetCurrent <level>
        await self.invoke(
            vid,
            "CurrentSensor.SetCurrentSW" if sw else "CurrentSensor.SetCurrent",
            value,
        )
