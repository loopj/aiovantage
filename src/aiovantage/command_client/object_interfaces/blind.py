"""Interface for querying and controlling blinds."""

from decimal import Decimal
from typing import NamedTuple

from .base import Interface, InterfaceResponse, fixed_result, fixed_to_decimal


class BlindInterface(Interface):
    """Interface for querying and controlling blinds."""

    class BlindState(NamedTuple):
        """The state of a blind."""

        is_moving: bool
        start_pos: Decimal
        end_pos: Decimal
        transition_time: Decimal
        start_time: int

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
        response = await self.invoke(vid, "Blind.GetPosition")
        return self.parse_get_position_response(response)

    async def get_position_hw(self, vid: int) -> Decimal:
        """Get the position of a blind directly from the hardware.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPositionHW
        response = await self.invoke(vid, "Blind.GetPositionHW")
        return self.parse_get_position_response(response)

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
        response = await self.invoke(vid, "Blind.GetTiltAngle")
        return self.parse_get_tilt_angle_response(response)

    async def get_tilt_angle_hw(self, vid: int) -> int:
        """Get the tilt angle of a blind directly from the hardware.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngleHW
        response = await self.invoke(vid, "Blind.GetTiltAngleHW")
        return self.parse_get_tilt_angle_response(response)

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
        response = await self.invoke(vid, "Blind.IsTiltAvailable")
        return self.parse_is_tilt_available_response(response)

    async def get_state(self, vid: int) -> BlindState:
        """Get the state of a blind.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The state of the blind.
        """
        # INVOKE <id> Blind.GetBlindState
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        response = await self.invoke(vid, "Blind.GetBlindState")
        return self.parse_get_state_response(response)

    @classmethod
    def parse_get_position_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Blind.GetPosition' response."""
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        # -> S:STATUS <id> Blind.GetPosition <position (0-100000)>
        # -> EL: <id> Blind.GetPosition <position (0-100000)>
        return fixed_result(response)

    @classmethod
    def parse_get_tilt_angle_response(cls, response: InterfaceResponse) -> int:
        """Parse a 'Blind.GetTiltAngle' response."""
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngle
        # -> S:STATUS <id> Blind.GetTiltAngle <angle (-100-100)>
        # -> EL: <id> Blind.GetTiltAngle <angle (-100-100)>
        return int(response.result)

    @classmethod
    def parse_is_tilt_available_response(cls, response: InterfaceResponse) -> bool:
        """Parse a 'Blind.IsTiltAvailable' response."""
        # -> R:INVOKE <id> <available (0/1)> Blind.IsTiltAvailable
        # -> S:STATUS <id> Blind.IsTiltAvailable <available (0/1)>
        # -> EL: <id> Blind.IsTiltAvailable <available (0/1)>
        return bool(int(response.result))

    @classmethod
    def parse_get_state_response(cls, response: InterfaceResponse) -> BlindState:
        """Parse a 'Blind.GetBlindState' response."""
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        # -> S:STATUS <id> Blind.GetBlindState <moving> <start> <end> <transitionTime> <startTime>
        # -> EL: <id> Blind.GetBlindState <moving> <start> <end> <transitionTime> <startTime>
        return cls.BlindState(
            # Is the blind currently moving?
            is_moving=bool(int(response.result)),
            # Position the blind is moving from (as a percentage)
            start_pos=fixed_to_decimal(response.args[0]),
            # Position the blind is moving to (as a percentage)
            end_pos=fixed_to_decimal(response.args[1]),
            # Time the blind will take to move (in seconds)
            transition_time=fixed_to_decimal(response.args[2]),
            # Time the blind started moving (in milliseconds since start of UTC day)
            start_time=int(response.args[3]),
        )
