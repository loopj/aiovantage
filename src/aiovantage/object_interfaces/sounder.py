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
        "Sounder.GetStatus": Status,
        "Sounder.GetStatusHW": Status,
    }

    # Methods
    async def get_frequency(self) -> Decimal:
        """Get the frequency of the keypad speaker, using cached value if available.

        Returns:
            The frequency of the keypad speaker in Hz.
        """
        # INVOKE <id> Sounder.GetFrequency
        # -> R:INVOKE <id> <frequency> Sounder.GetFrequency
        return await self.invoke("Sounder.GetFrequency", as_type=Decimal)

    async def get_frequency_hw(self) -> Decimal:
        """Get the frequency of the keypad speaker directly from the hardware.

        Returns:
            The frequency of the keypad speaker in Hz.
        """
        # INVOKE <id> Sounder.GetFrequencyHW
        # -> R:INVOKE <id> <frequency> Sounder.GetFrequency
        return await self.invoke("Sounder.GetFrequencyHW", as_type=Decimal)

    async def set_frequency(self, frequency: float | Decimal) -> None:
        """Set the frequency of the keypad speaker.

        Args:
            frequency: The frequency to set the sounder to, in Hz.
        """
        # INVOKE <id> Sounder.SetFrequency <frequency>
        # -> R:INVOKE <id> <rcode> Sounder.SetFrequency
        await self.invoke("Sounder.SetFrequency", frequency)

    async def get_status(self) -> Status:
        """Get the status of the keypad speaker, using cached value if available.

        Returns:
            The status of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetStatus
        # -> R:INVOKE <id> <status (0/1)> Sounder.GetStatus
        return await self.invoke("Sounder.GetStatus", as_type=self.Status)

    async def get_status_hw(self) -> Status:
        """Get the status of the keypad speaker directly from the hardware.

        Returns:
            The status of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetStatusHW
        # -> R:INVOKE <id> <status (0/1)> Sounder.GetStatus
        return await self.invoke("Sounder.GetStatusHW", as_type=self.Status)

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

    # Additional convenience methods, not part of the Vantage API
    async def turn_on(self) -> None:
        """Turn on the keypad speaker."""
        await self.set_status(self.Status.On)

    async def turn_off(self) -> None:
        """Turn off the keypad speaker."""
        await self.set_status(self.Status.Off)
