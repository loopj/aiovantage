"""Interface for querying and controlling blinds."""

from decimal import Decimal
from typing import NamedTuple

from .base import Interface


class BlindInterface(Interface):
    """Interface for querying and controlling blinds."""

    class BlindState(NamedTuple):
        """The state of a blind."""

        is_moving: bool
        start_pos: Decimal
        end_pos: Decimal
        transition_time: Decimal
        start_time: int

    class TravelTimes(NamedTuple):
        """The travel times of a blind."""

        rcode: int
        open_time: Decimal
        close_time: Decimal

    method_signatures = {
        "Blind.GetPosition": Decimal,
        "Blind.GetPositionHW": Decimal,
        "Blind.GetTiltAngle": int,
        "Blind.GetTiltAngleHW": int,
        "Blind.IsTiltAvailable": bool,
        "Blind.GetBlindState": BlindState,
        "Blind.GetUpperLimit": Decimal,
        "Blind.GetUpperLimitHW": Decimal,
        "Blind.GetLowerLimit": Decimal,
        "Blind.GetLowerLimitHW": Decimal,
        "Blind.GetTravelTimes": TravelTimes,
    }

    async def open(self, vid: int) -> None:
        """Open a blind.

        Args:
            vid: The Vantage ID of the blind.
        """
        # INVOKE <id> Blind.Open
        # -> R:INVOKE <id> <rcode> Blind.Open
        await self.invoke(vid, "Blind.Open")

    async def close(self, vid: int) -> None:
        """Close a blind.

        Args:
            vid: The Vantage ID of the blind.
        """
        # INVOKE <id> Blind.Close
        # -> R:INVOKE <id> <rcode> Blind.Close
        await self.invoke(vid, "Blind.Close")

    async def stop(self, vid: int) -> None:
        """Stop a blind.

        Args:
            vid: The Vantage ID of the blind.
        """
        # INVOKE <id> Blind.Stop
        # -> R:INVOKE <id> <rcode> Blind.Stop
        await self.invoke(vid, "Blind.Stop")

    async def set_position(
        self, vid: int, position: float, *, sw: bool = False
    ) -> None:
        """Set the position of a blind.

        Args:
            vid: The Vantage ID of the blind.
            position: The position to set the blind to, as a percentage.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetPosition <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPosition <position>
        await self.invoke(
            vid, "Blind.SetPositionSW" if sw else "Blind.SetPosition", position
        )

    async def get_position(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the position of a blind.

        Args:
            vid: The Vantage ID of the blind.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPosition
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        return await self.invoke(
            vid, "Blind.GetPositionHW" if hw else "Blind.GetPosition"
        )

    async def set_tilt_angle(self, vid: int, angle: int, *, sw: bool = False) -> None:
        """Set the tilt angle of a blind.

        Args:
            vid: The Vantage ID of the blind.
            angle: The angle to set the blind to, from -100 to 100.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetTiltAngle <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngle <angle>
        await self.invoke(
            vid, "Blind.SetTiltAngleSW" if sw else "Blind.SetTiltAngle", angle
        )

    async def get_tilt_angle(self, vid: int, *, hw: bool = False) -> int:
        """Get the tilt angle of a blind.

        Args:
            vid: The Vantage ID of the blind.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngle
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngle
        return await self.invoke(
            vid, "Blind.GetTiltAngleHW" if hw else "Blind.GetTiltAngle"
        )

    async def tilt_clockwise(self, vid: int, angle: int) -> None:
        """Tilt the blinds clockwise by the specified angle.

        Args:
            vid: The Vantage ID of the blind.
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltClockwise <angle>
        await self.invoke(vid, "Blind.TiltClockwise", angle)

    async def tilt_counter_clockwise(self, vid: int, angle: int) -> None:
        """Tilt the shades counter-clockwise by the specified angle.

        Args:
            vid: The Vantage ID of the blind.
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltCounterClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltCounterClockwise <angle>
        await self.invoke(vid, "Blind.TiltCounterClockwise", angle)

    async def is_tilt_available(self, vid: int) -> bool:
        """Check if the blind can tilt in its current state.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.IsTiltAvailable
        # -> R:INVOKE <id> <available (0/1)> Blind.IsTiltAvailable
        return await self.invoke(vid, "Blind.IsTiltAvailable")

    async def set_tilt_available(self, vid: int, available: bool) -> None:
        """Set the cached tilt availability of a blind.

        Args:
            vid: The Vantage ID of the blind.
            available: Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.SetTiltAvailableSW <available>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAvailableSW <available>
        await self.invoke(vid, "Blind.SetTiltAvailableSW", available)

    async def get_blind_state(self, vid: int) -> BlindState:
        """Get the state of a blind.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The state of the blind.
        """
        # INVOKE <id> Blind.GetBlindState
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        return await self.invoke(vid, "Blind.GetBlindState")

    async def set_upper_limit(
        self, vid: int, limit: Decimal, *, sw: bool = False
    ) -> None:
        """Set the upper limit of a blind.

        Args:
            vid: The Vantage ID of the blind.
            limit: The upper limit to set the blind to, as a percentage.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetUpperLimit <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetUpperLimit <limit>
        await self.invoke(
            vid, "Blind.SetUpperLimitSW" if sw else "Blind.SetUpperLimit", limit
        )

    async def get_upper_limit(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the upper limit of a blind.

        Args:
            vid: The Vantage ID of the blind.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The upper limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetUpperLimit
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetUpperLimit
        return await self.invoke(
            vid, "Blind.GetUpperLimitHW" if hw else "Blind.GetUpperLimit"
        )

    async def set_lower_limit(
        self, vid: int, limit: Decimal, *, sw: bool = False
    ) -> None:
        """Set the lower limit of a blind.

        Args:
            vid: The Vantage ID of the blind.
            limit: The lower limit to set the blind to, as a percentage.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetLowerLimit <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetLowerLimit <limit>
        await self.invoke(
            vid, "Blind.SetLowerLimitSW" if sw else "Blind.SetLowerLimit", limit
        )

    async def get_lower_limit(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the lower limit of a blind.

        Args:
            vid: The Vantage ID of the blind.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The lower limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetLowerLimit
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetLowerLimit
        return await self.invoke(
            vid, "Blind.GetLowerLimitHW" if hw else "Blind.GetLowerLimit"
        )

    async def get_travel_times(self, vid: int) -> TravelTimes:
        """Get the travel times of a blind.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The travel times of the blind.
        """
        # INVOKE <id> Blind.GetTravelTimes
        # -> R:INVOKE <id> <openTime> <closeTime> Blind.GetTravelTimes
        return await self.invoke(vid, "Blind.GetTravelTimes")
