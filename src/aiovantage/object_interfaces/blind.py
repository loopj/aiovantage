"""Interface for querying and controlling blinds."""

from decimal import Decimal
from typing import NamedTuple

from aiovantage.object_interfaces.interface_classes import ShadeOrientation, ShadeType

from .base import Interface, method


class BlindInterface(Interface, ShadeOrientation, ShadeType):
    """Interface for querying and controlling blinds."""

    # Types
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

    # Properties
    position: Decimal | None = None
    tilt_angle: int | None = None
    tilt_available: bool | None = None
    blind_state: BlindState | None = None
    upper_limit: Decimal | None = None
    lower_limit: Decimal | None = None
    travel_times: TravelTimes | None = None

    # Methods
    @method("Blind.Open")
    async def open(self) -> None:
        """Open a blind."""
        # INVOKE <id> Blind.Open
        # -> R:INVOKE <id> <rcode> Blind.Open
        await self.invoke("Blind.Open")

    @method("Blind.Close")
    async def close(self) -> None:
        """Close a blind."""
        # INVOKE <id> Blind.Close
        # -> R:INVOKE <id> <rcode> Blind.Close
        await self.invoke("Blind.Close")

    @method("Blind.Stop")
    async def stop(self) -> None:
        """Stop a blind."""
        # INVOKE <id> Blind.Stop
        # -> R:INVOKE <id> <rcode> Blind.Stop
        await self.invoke("Blind.Stop")

    @method("Blind.SetPosition")
    async def set_position(self, position: float) -> None:
        """Set the position of a blind.

        Args:
            position: The position to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetPosition <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPosition <position>
        await self.invoke("Blind.SetPosition", position)

    @method("Blind.GetPosition", property="position")
    async def get_position(self) -> Decimal:
        """Get the position of a blind, using cached value if available.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPosition
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        return await self.invoke("Blind.GetPosition")

    @method("Blind.GetPositionHW")
    async def get_position_hw(self) -> Decimal:
        """Get the position of a blind directly from the hardware.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPositionHW
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPositionHW
        return await self.invoke("Blind.GetPositionHW")

    @method("Blind.SetPositionSW")
    async def set_position_sw(self, position: Decimal) -> None:
        """Set the cached position of a blind.

        Args:
            position: The position to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetPositionSW <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPositionSW <position>
        await self.invoke("Blind.SetPositionSW", position)

    # Methods below here are not available in 2.x firmware.
    @method("Blind.SetTiltAngle")
    async def set_tilt_angle(self, angle: int) -> None:
        """Set the tilt angle of a blind.

        Args:
            angle: The angle to set the blind to, from -100 to 100.
        """
        # INVOKE <id> Blind.SetTiltAngle <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngle <angle>
        await self.invoke("Blind.SetTiltAngle", angle)

    @method("Blind.GetTiltAngle", property="tilt_angle")
    async def get_tilt_angle(self) -> int:
        """Get the tilt angle of a blind, using cached value if available.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngle
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngle
        return await self.invoke("Blind.GetTiltAngle")

    @method("Blind.SetTiltAngleSW")
    async def set_tilt_angle_sw(self, angle: int) -> None:
        """Set the cached tilt angle of a blind.

        Args:
            angle: The angle to set the blind to, from -100 to 100.
        """
        # INVOKE <id> Blind.SetTiltAngleSW <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngleSW <angle>
        await self.invoke("Blind.SetTiltAngleSW", angle)

    @method("Blind.GetTiltAngleHW")
    async def get_tilt_angle_hw(self) -> int:
        """Get the tilt angle of a blind directly from the hardware.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngleHW
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngleHW
        return await self.invoke("Blind.GetTiltAngleHW")

    @method("Blind.TiltClockwise")
    async def tilt_clockwise(self, angle: int) -> None:
        """Tilt the blinds clockwise by the specified angle.

        Args:
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltClockwise <angle>
        await self.invoke("Blind.TiltClockwise", angle)

    @method("Blind.TiltCounterClockwise")
    async def tilt_counter_clockwise(self, angle: int) -> None:
        """Tilt the shades counter-clockwise by the specified angle.

        Args:
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltCounterClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltCounterClockwise <angle>
        await self.invoke("Blind.TiltCounterClockwise", angle)

    @method("Blind.IsTiltAvailable", property="tilt_available")
    async def is_tilt_available(self) -> bool:
        """Check if the blind can tilt in its current state.

        Returns:
            Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.IsTiltAvailable
        # -> R:INVOKE <id> <available (0/1)> Blind.IsTiltAvailable
        return await self.invoke("Blind.IsTiltAvailable")

    @method("Blind.SetTiltAvailableSW")
    async def set_tilt_available_sw(self, available: bool) -> None:
        """Set the cached tilt availability of a blind.

        Args:
            available: Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.SetTiltAvailableSW <available>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAvailableSW <available>
        await self.invoke("Blind.SetTiltAvailableSW", available)

    @method("Blind.GetBlindState", property="blind_state")
    async def get_blind_state(self) -> BlindState:
        """Get the state of a blind.

        Returns:
            The state of the blind.
        """
        # INVOKE <id> Blind.GetBlindState
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        return await self.invoke("Blind.GetBlindState")

    @method("Blind.SetUpperLimit")
    async def set_upper_limit(self, limit: Decimal) -> None:
        """Set the upper limit of a blind.

        Args:
            limit: The upper limit to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetUpperLimit <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetUpperLimit <limit>
        await self.invoke("Blind.SetUpperLimit", limit)

    @method("Blind.GetUpperLimit", property="upper_limit")
    async def get_upper_limit(self) -> Decimal:
        """Get the upper limit of a blind.

        Returns:
            The upper limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetUpperLimit
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetUpperLimit
        return await self.invoke("Blind.GetUpperLimit")

    @method("Blind.GetUpperLimitHW")
    async def get_upper_limit_hw(self) -> Decimal:
        """Get the upper limit of a blind directly from the hardware.

        Returns:
            The upper limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetUpperLimitHW
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetUpperLimitHW
        return await self.invoke("Blind.GetUpperLimitHW")

    @method("Blind.SetUpperLimitSW")
    async def set_upper_limit_sw(self, limit: Decimal) -> None:
        """Set the cached upper limit of a blind.

        Args:
            limit: The upper limit to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetUpperLimitSW <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetUpperLimitSW <limit>
        await self.invoke("Blind.SetUpperLimitSW", limit)

    @method("Blind.SetLowerLimit")
    async def set_lower_limit(self, limit: Decimal) -> None:
        """Set the lower limit of a blind.

        Args:
            limit: The lower limit to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetLowerLimit <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetLowerLimit <limit>
        await self.invoke("Blind.SetLowerLimit", limit)

    @method("Blind.GetLowerLimit", property="lower_limit")
    async def get_lower_limit(self) -> Decimal:
        """Get the lower limit of a blind.

        Returns:
            The lower limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetLowerLimit
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetLowerLimit
        return await self.invoke("Blind.GetLowerLimit")

    @method("Blind.GetLowerLimitHW")
    async def get_lower_limit_hw(self) -> Decimal:
        """Get the lower limit of a blind directly from the hardware.

        Returns:
            The lower limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetLowerLimitHW
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetLowerLimitHW
        return await self.invoke("Blind.GetLowerLimitHW")

    @method("Blind.SetLowerLimitSW")
    async def set_lower_limit_sw(self, limit: Decimal) -> None:
        """Set the cached lower limit of a blind.

        Args:
            limit: The lower limit to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetLowerLimitSW <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetLowerLimitSW <limit>
        await self.invoke("Blind.SetLowerLimitSW", limit)

    @method("Blind.GetTravelTimes", property="travel_times")
    async def get_travel_times(self) -> TravelTimes:
        """Get the travel times of a blind.

        Returns:
            The travel times of the blind.
        """
        # INVOKE <id> Blind.GetTravelTimes
        # -> R:INVOKE <id> <openTime> <closeTime> Blind.GetTravelTimes
        return await self.invoke("Blind.GetTravelTimes")
