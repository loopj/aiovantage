"""Interface for querying and controlling blinds."""

from collections import namedtuple
from decimal import Decimal
from typing import Sequence

from .base import Interface


class BlindInterface(Interface):
    """Interface for querying and controlling blinds."""

    BlindState = namedtuple(
        "BlindState",
        ["is_moving", "start_pos", "end_pos", "transition_time", "start_time"],
    )

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

    async def get_position(self, vid: int) -> Decimal:
        """Get the position of a blind.

        Args:
            vid: The Vantage ID of the blind.

        Returns:
            The position of the blind, as a percentage.
        """
        # INVOKE <id> Blind.GetPosition
        # -> R:INVOKE <id> <position (0-100.000)> Blind.GetPosition
        response = await self.invoke(vid, "Blind.GetPosition")
        position = Decimal(response.args[1])

        return position

    async def set_position(self, vid: int, position: float) -> None:
        """Set the position of a blind.

        Args:
            vid: The Vantage ID of the blind.
            position: The position to set the blind to, as a percentage.
        """
        # INVOKE <id> Blind.SetPosition <position>
        # -> R:INVOKE <id> <rcode> Blind.SetPosition <position>
        await self.invoke(vid, "Blind.SetPosition", position)

    @classmethod
    def parse_blind_status(cls, args: Sequence[str]) -> Decimal:
        """Parse a simple 'S:BLIND' event.

        Args:
            args: The arguments of the event.

        Returns:
            The position of the blind, as a percentage.
        """
        # STATUS BLIND
        # -> S:BLIND <id> <position (0-100.000)>
        return Decimal(args[0])

    @classmethod
    def parse_get_position_status(cls, args: Sequence[str]) -> Decimal:
        """Parse a 'Blind.GetPosition' event."""
        # ELLOG STATUS ON
        # -> EL: <id> Blind.GetPosition <position (0-100000)>

        # ADDSTATUS <id>
        # -> S:STATUS <id> Blind.GetPosition <position (0-100000)>
        position = Decimal(args[0]) / 1000

        return position

    @classmethod
    def parse_get_state_status(cls, args: Sequence[str]) -> BlindState:
        """Parse a 'Blind.GetBlindState' event."""
        # ADDSTATUS <id>
        # -> S:STATUS <id> Blind.GetBlindState <moving> <start> <end> <transitionTime> <startTime>

        # ELLOG STATUSEX ON
        # -> EL: <id> Blind.GetBlindState <moving> <start> <end> <transitionTime> <startTime>
        return cls.BlindState(
            # Is the blind currently moving?
            is_moving=bool(int(args[0])),
            # Position the blind is moving from (as a percentage)
            start_pos=Decimal(args[1]) / 1000,
            # Position the blind is moving to (as a percentage)
            end_pos=Decimal(args[2]) / 1000,
            # Time the blind will take to move (in seconds)
            transition_time=Decimal(args[3]) / 1000,
            # Time the blind started moving (in milliseconds since start of UTC day)
            start_time=int(args[4]),
        )
