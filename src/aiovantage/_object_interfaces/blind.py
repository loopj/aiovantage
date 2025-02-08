from dataclasses import dataclass, field
from decimal import Decimal

from typing_extensions import override

from .base import Interface, method
from .fields import ShadeOrientation, ShadeType


class BlindInterface(Interface, ShadeOrientation, ShadeType):
    """Blind object interface."""

    interface_name = "Blind"

    @dataclass
    class BlindState:
        """The state of a blind."""

        is_moving: bool = field(metadata={"out": "return"})
        start_pos: Decimal = field(metadata={"out": "arg0"})
        end_pos: Decimal = field(metadata={"out": "arg1"})
        transition_time: Decimal = field(metadata={"out": "arg2"})
        start_time: int = field(metadata={"out": "arg3"})

    @dataclass
    class TravelTimes:
        """The travel times of a blind."""

        open_time: Decimal = field(metadata={"out": "arg0"})
        close_time: Decimal = field(metadata={"out": "arg1"})

    # Properties
    position: Decimal | None = None
    tilt_angle: int | None = None
    tilt_available: bool | None = None
    blind_state: BlindState | None = None

    # Methods
    @method("Open")
    async def open(self) -> None:
        """Open a blind."""
        # INVOKE <id> Blind.Open
        # -> R:INVOKE <id> <rcode> Blind.Open
        await self.invoke("Blind.Open")

    @method("Close")
    async def close(self) -> None:
        """Close a blind."""
        # INVOKE <id> Blind.Close
        # -> R:INVOKE <id> <rcode> Blind.Close
        await self.invoke("Blind.Close")

    @method("Stop")
    async def stop(self) -> None:
        """Stop a blind."""
        # INVOKE <id> Blind.Stop
        # -> R:INVOKE <id> <rcode> Blind.Stop
        await self.invoke("Blind.Stop")

    @method("SetPosition", "SetPositionSW")
    async def set_position(self, position: float, *, sw: bool = False) -> None:
        """Set the position of a blind.

        Args:
            position: The position to set the blind to, as a percentage.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetPosition <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPosition <position>
        await self.invoke(
            "Blind.SetPositionSW" if sw else "Blind.SetPosition", position
        )

    @method("GetPosition", "GetPositionHW", property="position")
    async def get_position(self, *, hw: bool = False) -> Decimal:
        """Get the position of a blind.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPosition
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        return await self.invoke("Blind.GetPositionHW" if hw else "Blind.GetPosition")

    @method("SetTiltAngle", "SetTiltAngleSW")
    async def set_tilt_angle(self, angle: int, *, sw: bool = False) -> None:
        """Set the tilt angle of a blind.

        Args:
            angle: The angle to set the blind to, from -100 to 100.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetTiltAngle <angle>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAngle <angle>
        await self.invoke("Blind.SetTiltAngleSW" if sw else "Blind.SetTiltAngle", angle)

    @method("GetTiltAngle", "GetTiltAngleHW", property="tilt_angle")
    async def get_tilt_angle(self, *, hw: bool = False) -> int:
        """Get the tilt angle of a blind.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The tilt angle of the blind, from -100 to 100.
        """
        # INVOKE <id> Blind.GetTiltAngle
        # -> R:INVOKE <id> <angle (-100-100)> Blind.GetTiltAngle
        return await self.invoke("Blind.GetTiltAngleHW" if hw else "Blind.GetTiltAngle")

    @method("TiltClockwise")
    async def tilt_clockwise(self, angle: int) -> None:
        """Tilt the blinds clockwise by the specified angle.

        Args:
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltClockwise <angle>
        await self.invoke("Blind.TiltClockwise", angle)

    @method("TiltCounterClockwise")
    async def tilt_counter_clockwise(self, angle: int) -> None:
        """Tilt the shades counter-clockwise by the specified angle.

        Args:
            angle: The angle offset the blinds should be tilted.
        """
        # INVOKE <id> Blind.TiltCounterClockwise <angle>
        # -> R:INVOKE <id> <rcode> Blind.TiltCounterClockwise <angle>
        await self.invoke("Blind.TiltCounterClockwise", angle)

    @method("IsTiltAvailable", property="tilt_available")
    async def is_tilt_available(self) -> bool:
        """Check if the blind can tilt in its current state.

        Returns:
            Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.IsTiltAvailable
        # -> R:INVOKE <id> <available (0/1)> Blind.IsTiltAvailable
        return await self.invoke("Blind.IsTiltAvailable")

    @method("SetTiltAvailableSW")
    async def set_tilt_available(self, available: bool) -> None:
        """Set the cached tilt availability of a blind.

        Args:
            available: Whether the blind supports tilting.
        """
        # INVOKE <id> Blind.SetTiltAvailableSW <available>
        # -> R:INVOKE <id> <rcode> Blind.SetTiltAvailableSW <available>
        await self.invoke("Blind.SetTiltAvailableSW", available)

    @method("GetBlindState", property="blind_state")
    async def get_blind_state(self) -> BlindState:
        """Get the state of a blind.

        Returns:
            The state of the blind.
        """
        # INVOKE <id> Blind.GetBlindState
        # -> R:INVOKE <id> <moving> Blind.GetBlindState <start> <end> <transitionTime> <startTime>
        return await self.invoke("Blind.GetBlindState")

    @method("SetUpperLimit", "SetUpperLimitSW")
    async def set_upper_limit(self, limit: Decimal, *, sw: bool = False) -> None:
        """Set the upper limit of a blind.

        Args:
            limit: The upper limit to set the blind to, as a percentage.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetUpperLimit <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetUpperLimit <limit>
        await self.invoke(
            "Blind.SetUpperLimitSW" if sw else "Blind.SetUpperLimit", limit
        )

    @method("GetUpperLimit", "GetUpperLimitHW")
    async def get_upper_limit(self, *, hw: bool = False) -> Decimal:
        """Get the upper limit of a blind.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The upper limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetUpperLimit
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetUpperLimit
        return await self.invoke(
            "Blind.GetUpperLimitHW" if hw else "Blind.GetUpperLimit"
        )

    @method("SetLowerLimit", "SetLowerLimitSW")
    async def set_lower_limit(self, limit: Decimal, *, sw: bool = False) -> None:
        """Set the lower limit of a blind.

        Args:
            limit: The lower limit to set the blind to, as a percentage.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Blind.SetLowerLimit <limit>
        # -> R:INVOKE <id> <rcode> Blind.SetLowerLimit <limit>
        await self.invoke(
            "Blind.SetLowerLimitSW" if sw else "Blind.SetLowerLimit", limit
        )

    @method("GetLowerLimit", "GetLowerLimitHW")
    async def get_lower_limit(self, *, hw: bool = False) -> Decimal:
        """Get the lower limit of a blind.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The lower limit of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetLowerLimit
        # -> R:INVOKE <id> <limit (0-100.000)> Blind.GetLowerLimit
        return await self.invoke(
            "Blind.GetLowerLimitHW" if hw else "Blind.GetLowerLimit"
        )

    @method("GetTravelTimes")
    async def get_travel_times(self) -> TravelTimes:
        """Get the travel times of a blind.

        Returns:
            The travel times of the blind.
        """
        # INVOKE <id> Blind.GetTravelTimes
        # -> R:INVOKE <id> <openTime> <closeTime> Blind.GetTravelTimes
        return await self.invoke("Blind.GetTravelTimes")

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "BLIND":
            # STATUS BLIND
            # -> S:BLIND <id> <position (0.000 - 100.000)>
            return self.update_properties({"position": Decimal(args[0])})

        return super().handle_category_status(category, *args)
