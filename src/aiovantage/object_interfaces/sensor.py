"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface


class SensorInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Sensor.GetLevel": Decimal,
        "Sensor.GetLevelHW": Decimal,
    }

    # Properties
    level: int | Decimal | None = None

    # Methods
    async def get_level(self) -> Decimal:
        """Get the level of a sensor, using cached value if available.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevel
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        return await self.invoke("Sensor.GetLevel", as_type=Decimal)

    async def get_level_hw(self) -> Decimal:
        """Get the level of a sensor directly from the hardware.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevelHW
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevelHW
        return await self.invoke("Sensor.GetLevelHW", as_type=Decimal)

    async def set_level(self, level: Decimal) -> None:
        """Set the level of a sensor.

        Args:
            level: The level to set the sensor to.
        """
        # INVOKE <id> Sensor.SetLevel <level (0-100)>
        # -> R:INVOKE <id> <rcode> Sensor.SetLevel <level (0-100)>
        await self.invoke("Sensor.SetLevel", level)

    async def get_high_range(self) -> Decimal:
        """Get the high range of a sensor.

        Returns:
            The high range of the sensor.
        """
        # INVOKE <id> Sensor.GetHighRange
        # -> R:INVOKE <id> <high range> Sensor.GetHighRange
        return await self.invoke("Sensor.GetHighRange", as_type=Decimal)

    async def get_low_range(self) -> Decimal:
        """Get the low range of a sensor.

        Returns:
            The low range of the sensor.
        """
        # INVOKE <id> Sensor.GetLowRange
        # -> R:INVOKE <id> <low range> Sensor.GetLowRange
        return await self.invoke("Sensor.GetLowRange", as_type=Decimal)

    async def get_hold_on_time(self) -> Decimal:
        """Get the hold on time of a sensor.

        Returns:
            The hold on time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetHoldOnTime
        # -> R:INVOKE <id> <hold on time> Sensor.GetHoldOnTime
        return await self.invoke("Sensor.GetHoldOnTime", as_type=Decimal)

    async def is_tracking(self) -> bool:
        """Get whether the sensor is tracking.

        Returns:
            Whether the sensor is tracking.
        """
        # INVOKE <id> Sensor.IsTracking
        # -> R:INVOKE <id> <tracking (0/1)> Sensor.IsTracking
        return await self.invoke("Sensor.IsTracking", as_type=bool)

    async def get_tracking_delta(self) -> Decimal:
        """Get the tracking delta of a sensor.

        Returns:
            The tracking delta of the sensor.
        """
        # INVOKE <id> Sensor.GetTrackingDelta
        # -> R:INVOKE <id> <tracking delta> Sensor.GetTrackingDelta
        return await self.invoke("Sensor.GetTrackingDelta", as_type=Decimal)

    async def get_tracking_min(self) -> Decimal:
        """Get the tracking min time of a sensor.

        Returns:
            The tracking min time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetTrackingMin
        # -> R:INVOKE <id> <tracking min> Sensor.GetTrackingMin
        return await self.invoke("Sensor.GetTrackingMin", as_type=Decimal)

    async def get_tracking_max(self) -> Decimal:
        """Get the tracking max time of a sensor.

        Returns:
            The tracking max time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetTrackingMax
        # -> R:INVOKE <id> <tracking max> Sensor.GetTrackingMax
        return await self.invoke("Sensor.GetTrackingMax", as_type=Decimal)
