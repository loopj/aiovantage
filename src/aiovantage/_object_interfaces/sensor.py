from decimal import Decimal

from .base import Interface, method


class SensorInterface(Interface):
    """Sensor interface."""

    interface_name = "Sensor"

    # Properties
    level: Decimal | None = None

    # Methods
    @method("GetLevel", "GetLevelHW", property="level")
    async def get_level(self, *, hw: bool = False) -> Decimal:
        """Get the level of a sensor.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevel
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        return await self.invoke("Sensor.GetLevelHW" if hw else "Sensor.GetLevel")

    @method("SetLevel")
    async def set_level(self, level: Decimal) -> None:
        """Set the level of a sensor.

        Args:
            level: The level to set the sensor to.
        """
        # INVOKE <id> Sensor.SetLevel <level (0-100)>
        # -> R:INVOKE <id> <rcode> Sensor.SetLevel <level (0-100)>
        await self.invoke("Sensor.SetLevel", level)

    @method("GetHighRange")
    async def get_high_range(self) -> Decimal:
        """Get the high range of a sensor.

        Returns:
            The high range of the sensor.
        """
        # INVOKE <id> Sensor.GetHighRange
        # -> R:INVOKE <id> <high range> Sensor.GetHighRange
        return await self.invoke("Sensor.GetHighRange")

    @method("GetLowRange")
    async def get_low_range(self) -> Decimal:
        """Get the low range of a sensor.

        Returns:
            The low range of the sensor.
        """
        # INVOKE <id> Sensor.GetLowRange
        # -> R:INVOKE <id> <low range> Sensor.GetLowRange
        return await self.invoke("Sensor.GetLowRange")

    @method("GetHoldOnTime")
    async def get_hold_on_time(self) -> Decimal:
        """Get the hold on time of a sensor.

        Returns:
            The hold on time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetHoldOnTime
        # -> R:INVOKE <id> <hold on time> Sensor.GetHoldOnTime
        return await self.invoke("Sensor.GetHoldOnTime")

    @method("IsTracking")
    async def is_tracking(self) -> bool:
        """Get whether the sensor is tracking.

        Returns:
            Whether the sensor is tracking.
        """
        # INVOKE <id> Sensor.IsTracking
        # -> R:INVOKE <id> <tracking (0/1)> Sensor.IsTracking
        return await self.invoke("Sensor.IsTracking")

    @method("GetTrackingDelta")
    async def get_tracking_delta(self) -> Decimal:
        """Get the tracking delta of a sensor.

        Returns:
            The tracking delta of the sensor.
        """
        # INVOKE <id> Sensor.GetTrackingDelta
        # -> R:INVOKE <id> <tracking delta> Sensor.GetTrackingDelta
        return await self.invoke("Sensor.GetTrackingDelta")

    @method("GetTrackingMin")
    async def get_tracking_min(self) -> Decimal:
        """Get the tracking min time of a sensor.

        Returns:
            The tracking min time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetTrackingMin
        # -> R:INVOKE <id> <tracking min> Sensor.GetTrackingMin
        return await self.invoke("Sensor.GetTrackingMin")

    @method("GetTrackingMax")
    async def get_tracking_max(self) -> Decimal:
        """Get the tracking max time of a sensor.

        Returns:
            The tracking max time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetTrackingMax
        # -> R:INVOKE <id> <tracking max> Sensor.GetTrackingMax
        return await self.invoke("Sensor.GetTrackingMax")
