"""Interface for querying and controlling sensors."""

from decimal import Decimal

from .base import Interface


class SensorInterface(Interface):
    """Interface for querying and controlling sensors."""

    method_signatures = {
        "Sensor.GetLevel": Decimal,
        "Sensor.GetLevelHW": Decimal,
        "Sensor.GetHighRange": Decimal,
        "Sensor.GetLowRange": Decimal,
        "Sensor.GetHoldOnTime": Decimal,
        "Sensor.IsTracking": bool,
        "Sensor.GetTrackingDelta": Decimal,
        "Sensor.GetTrackingMin": Decimal,
        "Sensor.GetTrackingMax": Decimal,
    }

    async def get_level(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the level of a sensor.

        Args:
            vid: The Vantage ID of the sensor.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The level of the sensor.
        """
        # INVOKE <id> Sensor.GetLevel
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        return await self.invoke(vid, "Sensor.GetLevelHW" if hw else "Sensor.GetLevel")

    async def set_level(self, vid: int, level: Decimal) -> None:
        """Set the level of a sensor.

        Args:
            vid: The Vantage ID of the sensor.
            level: The level to set the sensor to.
        """
        # INVOKE <id> Sensor.SetLevel <level (0-100)>
        # -> R:INVOKE <id> <rcode> Sensor.SetLevel <level (0-100)>
        await self.invoke(vid, "Sensor.SetLevel", level)

    async def get_high_range(self, vid: int) -> Decimal:
        """Get the high range of a sensor.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The high range of the sensor.
        """
        # INVOKE <id> Sensor.GetHighRange
        # -> R:INVOKE <id> <high range> Sensor.GetHighRange
        return await self.invoke(vid, "Sensor.GetHighRange")

    async def get_low_range(self, vid: int) -> Decimal:
        """Get the low range of a sensor.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The low range of the sensor.
        """
        # INVOKE <id> Sensor.GetLowRange
        # -> R:INVOKE <id> <low range> Sensor.GetLowRange
        return await self.invoke(vid, "Sensor.GetLowRange")

    async def get_hold_on_time(self, vid: int) -> Decimal:
        """Get the hold on time of a sensor.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The hold on time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetHoldOnTime
        # -> R:INVOKE <id> <hold on time> Sensor.GetHoldOnTime
        return await self.invoke(vid, "Sensor.GetHoldOnTime")

    async def is_tracking(self, vid: int) -> bool:
        """Get whether the sensor is tracking.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            Whether the sensor is tracking.
        """
        # INVOKE <id> Sensor.IsTracking
        # -> R:INVOKE <id> <tracking (0/1)> Sensor.IsTracking
        return await self.invoke(vid, "Sensor.IsTracking")

    async def get_tracking_delta(self, vid: int) -> Decimal:
        """Get the tracking delta of a sensor.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The tracking delta of the sensor.
        """
        # INVOKE <id> Sensor.GetTrackingDelta
        # -> R:INVOKE <id> <tracking delta> Sensor.GetTrackingDelta
        return await self.invoke(vid, "Sensor.GetTrackingDelta")

    async def get_tracking_min(self, vid: int) -> Decimal:
        """Get the tracking min time of a sensor.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The tracking min time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetTrackingMin
        # -> R:INVOKE <id> <tracking min> Sensor.GetTrackingMin
        return await self.invoke(vid, "Sensor.GetTrackingMin")

    async def get_tracking_max(self, vid: int) -> Decimal:
        """Get the tracking max time of a sensor.

        Args:
            vid: The Vantage ID of the sensor.

        Returns:
            The tracking max time of the sensor, in seconds.
        """
        # INVOKE <id> Sensor.GetTrackingMax
        # -> R:INVOKE <id> <tracking max> Sensor.GetTrackingMax
        return await self.invoke(vid, "Sensor.GetTrackingMax")
