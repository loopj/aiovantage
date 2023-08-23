"""Interface for keypad speakers."""

from .base import Interface


class SounderInterface(Interface):
    """Interface for keypad speakers."""

    async def turn_on(self, vid: int) -> None:
        """Turn on the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
        """
        # INVOKE <id> Sounder.TurnOn
        # -> R:INVOKE <id> <rcode> Sounder.SetStatus
        await self.invoke(vid, "Sounder.SetStatus", "On")

    async def turn_off(self, vid: int) -> None:
        """Turn off the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
        """
        # INVOKE <id> Sounder.TurnOff
        # -> R:INVOKE <id> <rcode> Sounder.SetStatus
        await self.invoke(vid, "Sounder.SetStatus", "Off")

    async def get_frequency(self, vid: int) -> float:
        """Get the frequency of the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.

        Returns:
            The frequency of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetFrequency
        # -> R:INVOKE <id> <frequency> Sounder.GetFrequency
        response = await self.invoke(vid, "Sounder.GetFrequency")
        frequency = float(response.args[0])

        return frequency

    async def set_frequency(self, vid: int, frequency: float) -> None:
        """Set the frequency of the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
            frequency: The frequency to set.
        """
        # INVOKE <id> Sounder.SetFrequency <frequency>
        # -> R:INVOKE <id> <rcode> Sounder.SetFrequency
        await self.invoke(vid, "Sounder.SetFrequency", frequency)

    # Not available in 2.x firmware
    async def play_fx(
        self, vid: int, effect: int, duration: float = 0, volume: float = 0
    ) -> None:
        """Play a sound effect on the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
            effect: The effect to play.
            duration: The duration to play the FX for, in seconds, 0 for default.
            volume: The volume to play the FX at, as a percentage, 0 for default.
        """
        # INVOKE <id> Sounder.PlayFX <fx> <duration> <volume>
        # -> R:INVOKE <id> <rcode> Sounder.PlayFX
        await self.invoke(vid, "Sounder.PlayFX", effect, duration, volume)
