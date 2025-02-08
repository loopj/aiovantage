from decimal import Decimal
from enum import IntEnum

from .base import Interface, method


class SounderInterface(Interface):
    """Sounder interface."""

    interface_name = "Sounder"

    class Status(IntEnum):
        """Sounder status."""

        On = 0
        Off = 1

    # Methods
    @method("GetFrequency", "GetFrequencyHW")
    async def get_frequency(self, *, hw: bool = False) -> Decimal:
        """Get the frequency of the keypad speaker.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The frequency of the keypad speaker in Hz.
        """
        # INVOKE <id> Sounder.GetFrequency
        # -> R:INVOKE <id> <frequency> Sounder.GetFrequency
        return await self.invoke(
            "Sounder.GetFrequencyHW" if hw else "Sounder.GetFrequency"
        )

    @method("SetFrequency")
    async def set_frequency(self, frequency: float | Decimal) -> None:
        """Set the frequency of the keypad speaker.

        Args:
            frequency: The frequency to set the sounder to, in Hz.
        """
        # INVOKE <id> Sounder.SetFrequency <frequency>
        # -> R:INVOKE <id> <rcode> Sounder.SetFrequency
        await self.invoke("Sounder.SetFrequency", frequency)

    @method("GetDuration", "GetDurationHW")
    async def get_duration(self, *, hw: bool = False) -> Decimal:
        """Get the length of time the keypad speaker will sound.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The duration of the keypad speaker sound in seconds.
        """
        # INVOKE <id> Sounder.GetDuration
        # -> R:INVOKE <id> <duration> Sounder.GetDuration
        return await self.invoke(
            "Sounder.GetDurationHW" if hw else "Sounder.GetDuration"
        )

    @method("SetDuration")
    async def set_duration(self, duration: Decimal) -> None:
        """Set the length of time the keypad speaker will sound.

        Args:
            duration: The duration to set the sounder to, in seconds.
        """
        # INVOKE <id> Sounder.SetDuration <duration>
        # -> R:INVOKE <id> <rcode> Sounder.SetDuration
        await self.invoke("Sounder.SetDuration", duration)

    async def get_status(self, *, hw: bool = False) -> Status:
        """Get the status of the keypad speaker.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The status of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetStatus
        # -> R:INVOKE <id> <status (0/1)> Sounder.GetStatus
        return await self.invoke("Sounder.GetStatusHW" if hw else "Sounder.GetStatus")

    async def set_status(self, status: Status) -> None:
        """Set the status of the keypad speaker.

        Args:
            status: The status to set the keypad speaker to.
        """
        # INVOKE <id> Sounder.SetStatus <status (0/1/On/Off)>
        # -> R:INVOKE <id> <rcode> Sounder.SetStatus
        await self.invoke("Sounder.SetStatus", status)

    async def play_fx(
        self, effect: int, duration: float = 0, volume: float = 0
    ) -> None:
        """Play a sound effect on the keypad speaker.

        Args:
            effect: The effect to play.
            duration: The duration to play the FX for, in seconds, 0 for default.
            volume: The volume to play the FX at, as a percentage, 0 for default.
        """
        # INVOKE <id> Sounder.PlayFX <fx> <duration> <volume>
        # -> R:INVOKE <id> <rcode> Sounder.PlayFX
        await self.invoke("Sounder.PlayFX", effect, duration, volume)

    # Convenience functions, not part of the interface
    async def turn_on(self) -> None:
        """Turn on the keypad speaker."""
        await self.set_status(self.Status.On)

    async def turn_off(self) -> None:
        """Turn off the keypad speaker."""
        await self.set_status(self.Status.Off)
