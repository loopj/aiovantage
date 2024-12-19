"""Interface for querying and controlling blinds."""

from decimal import Decimal
from typing import NamedTuple

from aiovantage.object_interfaces.interface_classes import (
    ShadeOrientation,
    ShadeType,
    WidgetPrecludable,
)

from .base import Interface


class BlindInterface(Interface, ShadeOrientation, ShadeType, WidgetPrecludable):
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

    # Properties
    position: Decimal | None = None
    tilt_angle: int | None = None
    tilt_available: bool | None = None
    blind_state: BlindState | None = None

    # Methods
    async def open(self) -> None:
        """Open a blind."""
        # INVOKE <id> Blind.Open
        # -> R:INVOKE <id> <rcode> Blind.Open
        await self.invoke("Blind.Open")

    async def close(self) -> None:
        """Close a blind."""
        # INVOKE <id> Blind.Close
        # -> R:INVOKE <id> <rcode> Blind.Close
        await self.invoke("Blind.Close")

    async def stop(self) -> None:
        """Stop a blind."""
        # INVOKE <id> Blind.Stop
        # -> R:INVOKE <id> <rcode> Blind.Stop
        await self.invoke("Blind.Stop")

    async def set_position(self, position: float) -> None:
        """Set the position of a blind.

        Args:
            position: The position to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetPosition <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPosition <position>
        await self.invoke("Blind.SetPosition", position)

    async def get_position(self) -> Decimal:
        """Get the position of a blind, using cached value if available.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPosition
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        return await self.invoke("Blind.GetPosition", as_type=Decimal)

    async def get_position_hw(self) -> Decimal:
        """Get the position of a blind directly from the hardware.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPositionHW
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPositionHW
        return await self.invoke("Blind.GetPositionHW", as_type=Decimal)

    async def set_position_sw(self, position: Decimal) -> None:
        """Set the cached position of a blind.

        Args:
            position: The position to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetPositionSW <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPositionSW <position>
        await self.invoke("Blind.SetPositionSW", position)

    # Methods below here are not available in 2.x firmware.
    async def set_tilt_angle(self, angle: int) -> None:
        """Set the tilt angle of a blind.

        Args:
            angle: The angle to set the blind to, from -100 to 100.
        """
        # INVOKE <id> Blind.SetTiltAngle <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngle <angle>
        await self.invoke("Blind.SetTiltAngle", angle)

    async def get_tilt_angle(self) -> int:
        """Get the tilt angle of a blind, using cached value if available.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngle
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngle
        return await self.invoke("Blind.GetTiltAngle", as_type=int)

    async def set_tilt_angle_sw(self, angle: int) -> None:
        """Set the cached tilt angle of a blind.

        Args:
            angle: The angle to set the blind to, from -100 to 100.
        """
        # INVOKE <id> Blind.SetTiltAngleSW <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngleSW <angle>
        await self.invoke("Blind.SetTiltAngleSW", angle)

    async def get_tilt_angle_hw(self) -> int:
        """Get the tilt angle of a blind directly from the hardware.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngleHW
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngleHW
        return await self.invoke("Blind.GetTiltAngleHW", as_type=int)

    async def tilt_clockwise(self, angle: int) -> None:
        """Tilt the blinds clockwise by the specified angle.

        Args:
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltClockwise <angle>
        await self.invoke("Blind.TiltClockwise", angle)

    async def tilt_counter_clockwise(self, angle: int) -> None:
        """Tilt the shades counter-clockwise by the specified angle.

        Args:
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltCounterClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltCounterClockwise <angle>
        await self.invoke("Blind.TiltCounterClockwise", angle)

    async def is_tilt_available(self) -> bool:
        """Check if the blind can tilt in its current state.

        Returns:
            Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.IsTiltAvailable
        # -> R:INVOKE <id> <available (0/1)> Blind.IsTiltAvailable
        return await self.invoke("Blind.IsTiltAvailable", as_type=bool)

    async def set_tilt_available_sw(self, available: bool) -> None:
        """Set the cached tilt availability of a blind.

        Args:
            available: Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.SetTiltAvailableSW <available>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAvailableSW <available>
        await self.invoke("Blind.SetTiltAvailableSW", available)

    async def get_blind_state(self) -> BlindState:
        """Get the state of a blind.

        Returns:
            The state of the blind.
        """
        # INVOKE <id> Blind.GetBlindState
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        return await self.invoke(
            "Blind.GetBlindState", as_type=BlindInterface.BlindState
        )
