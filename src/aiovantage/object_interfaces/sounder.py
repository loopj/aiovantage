"""Interface for keypad speakers."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class SounderInterface(Interface):
    """Interface for keypad speakers."""

    class Status(IntEnum):
        """Sounder status."""

        On = 0
        Off = 1

    method_signatures = {
        "Sounder.GetFrequency": Decimal,
        "Sounder.GetFrequencyHW": Decimal,
        "Sounder.GetDuration": Decimal,
        "Sounder.GetDurationHW": Decimal,
        "Sounder.GetStatus": Status,
        "Sounder.GetStatusHW": Status,
    }

    async def get_frequency(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the frequency of the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The frequency of the keypad speaker in Hz.
        """
        # INVOKE <id> Sounder.GetFrequency
        # -> R:INVOKE <id> <frequency> Sounder.GetFrequency
        return await self.invoke(
            vid, "Sounder.GetFrequencyHW" if hw else "Sounder.GetFrequency"
        )

    async def set_frequency(self, vid: int, frequency: float | Decimal) -> None:
        """Set the frequency of the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
            frequency: The frequency to set the sounder to, in Hz.
        """
        # INVOKE <id> Sounder.SetFrequency <frequency>
        # -> R:INVOKE <id> <rcode> Sounder.SetFrequency
        await self.invoke(vid, "Sounder.SetFrequency", frequency)

    async def get_duration(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the length of time the keypad speaker will sound.

        Args:
            vid: The Vantage ID of the sounder.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The duration of the keypad speaker sound in seconds.
        """
        # INVOKE <id> Sounder.GetDuration
        # -> R:INVOKE <id> <duration> Sounder.GetDuration
        return await self.invoke(
            vid, "Sounder.GetDurationHW" if hw else "Sounder.GetDuration"
        )

    async def set_duration(self, vid: int, duration: Decimal) -> None:
        """Set the length of time the keypad speaker will sound.

        Args:
            vid: The Vantage ID of the sounder.
            duration: The duration to set the sounder to, in seconds.
        """
        # INVOKE <id> Sounder.SetDuration <duration>
        # -> R:INVOKE <id> <rcode> Sounder.SetDuration
        await self.invoke(vid, "Sounder.SetDuration", duration)

    async def get_status(self, vid: int, *, hw: bool = False) -> Status:
        """Get the status of the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The status of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetStatus
        # -> R:INVOKE <id> <status (0/1)> Sounder.GetStatus
        return await self.invoke(
            vid, "Sounder.GetStatusHW" if hw else "Sounder.GetStatus"
        )

    async def set_status(self, vid: int, status: Status) -> None:
        """Set the status of the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
            status: The status to set the keypad speaker to.
        """
        # INVOKE <id> Sounder.SetStatus <status (0/1/On/Off)>
        # -> R:INVOKE <id> <rcode> Sounder.SetStatus
        await self.invoke(vid, "Sounder.SetStatus", status)

    async def play_fx(
        self, vid: int, effect: int, duration: float = 0, volume: float = 0
    ) -> None:
        """Play a sound effect on the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
            effect: The effect to play.
            duration: The duration to play the FX for, in seconds, 0 for default.
            volume: The volume to play the FX at, as a percentage, 0 for default.
        """
        # INVOKE <id> Sounder.PlayFX <fx> <duration> <volume>
        # -> R:INVOKE <id> <rcode> Sounder.PlayFX
        await self.invoke(vid, "Sounder.PlayFX", effect, duration, volume)

    # Convenience functions, not part of the interface
    async def turn_on(self, vid: int) -> None:
        """Turn on the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
        """
        await self.set_status(vid, self.Status.On)

    async def turn_off(self, vid: int) -> None:
        """Turn off the keypad speaker.

        Args:
            vid: The Vantage ID of the sounder.
        """
        await self.set_status(vid, self.Status.Off)
