"""Interface for querying and controlling blinds."""

from decimal import Decimal
from typing import NamedTuple

from .base import Interface


class BlindInterface(Interface):
    """Interface for querying and controlling blinds."""

    class BlindState(NamedTuple):
        """The state of a blind."""

        is_moving: bool
        """Is the blind currently moving?"""

        start_pos: Decimal
        """Position the blind is moving from (as a percentage)"""

        end_pos: Decimal
        """Position the blind is moving to (as a percentage)"""

        transition_time: Decimal
        """Time the blind will take to move (in seconds)"""

        start_time: int
        """Time the blind started moving (in milliseconds since start of UTC day)"""

    method_signatures = {
        "Blind.GetPosition": Decimal,
        "Blind.GetPositionHW": Decimal,
        "Blind.GetTiltAngle": int,
        "Blind.GetTiltAngleHW": int,
        "Blind.IsTiltAvailable": bool,
        "Blind.GetBlindState": BlindState,
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

    async def set_position(self, vid: int, position: float) -> None:
        """Set the position of a blind.

        Args:
            vid: The Vantage ID of the blind.
            position: The position to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetPosition <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPosition <position>
        await self.invoke(vid, "Blind.SetPosition", position)

    async def get_position(self, vid: int) -> Decimal:
        """Get the position of a blind, using cached value if available.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPosition
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        return await self.invoke(vid, "Blind.GetPosition", as_type=Decimal)

    async def get_position_hw(self, vid: int) -> Decimal:
        """Get the position of a blind directly from the hardware.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPositionHW
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPositionHW
        return await self.invoke(vid, "Blind.GetPositionHW", as_type=Decimal)

    # Methods below here are not available in 2.x firmware.
    async def set_tilt_angle(self, vid: int, angle: int) -> None:
        """Set the tilt angle of a blind.

        Args:
            vid: The Vantage ID of the blind.
            angle: The angle to set the blind to, from -100 to 100.
        """
        # INVOKE <id> Blind.SetTiltAngle <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngle <angle>
        await self.invoke(vid, "Blind.SetTiltAngle", angle)

    async def get_tilt_angle(self, vid: int) -> int:
        """Get the tilt angle of a blind, using cached value if available.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngle
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngle
        return await self.invoke(vid, "Blind.GetTiltAngle", as_type=int)

    async def get_tilt_angle_hw(self, vid: int) -> int:
        """Get the tilt angle of a blind directly from the hardware.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngleHW
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngleHW
        return await self.invoke(vid, "Blind.GetTiltAngleHW", as_type=int)

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
        return await self.invoke(vid, "Blind.IsTiltAvailable", as_type=bool)

    async def get_blind_state(self, vid: int) -> BlindState:
        """Get the state of a blind.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The state of the blind.
        """
        # INVOKE <id> Blind.GetBlindState
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        return await self.invoke(vid, "Blind.GetBlindState", as_type=self.BlindState)
