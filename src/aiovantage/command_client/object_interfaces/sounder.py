"""Interface for keypad speakers."""

from decimal import Decimal
from enum import IntEnum
from typing import Union

from .base import Interface, InterfaceResponse, enum_result, fixed_result


class SounderInterface(Interface):
    """Interface for keypad speakers."""

    class Status(IntEnum):
        """Sounder status."""

        ON = 0
        OFF = 1

    async def get_frequency(self, vid: int) -> Decimal:
        """Get the frequency of the keypad speaker, using cached value if available.

        Args:
            vid: The Vantage ID of the keypad.

        Returns:
            The frequency of the keypad speaker in Hz.
        """
        # INVOKE <id> Sounder.GetFrequency
        response = await self.invoke(vid, "Sounder.GetFrequency")
        return self.parse_get_frequency_response(response)

    async def get_frequency_hw(self, vid: int) -> Decimal:
        """Get the frequency of the keypad speaker directly from the hardware.

        Args:
            vid: The Vantage ID of the keypad.

        Returns:
            The frequency of the keypad speaker in Hz.
        """
        # INVOKE <id> Sounder.GetFrequencyHW
        response = await self.invoke(vid, "Sounder.GetFrequencyHW")
        return self.parse_get_frequency_response(response)

    async def set_frequency(self, vid: int, frequency: Union[float, Decimal]) -> None:
        """Set the frequency of the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
            frequency: The frequency to set the sounder to, in Hz.
        """
        # INVOKE <id> Sounder.SetFrequency <frequency>
        # -> R:INVOKE <id> <rcode> Sounder.SetFrequency
        await self.invoke(vid, "Sounder.SetFrequency", frequency)

    async def get_status(self, vid: int) -> Status:
        """Get the status of the keypad speaker, using cached value if available.

        Args:
            vid: The Vantage ID of the keypad.

        Returns:
            The status of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetStatus
        response = await self.invoke(vid, "Sounder.GetStatus")
        return self.parse_get_status_response(response)

    async def get_status_hw(self, vid: int) -> Status:
        """Get the status of the keypad speaker directly from the hardware.

        Args:
            vid: The Vantage ID of the keypad.

        Returns:
            The status of the keypad speaker.
        """
        # INVOKE <id> Sounder.GetStatusHW
        response = await self.invoke(vid, "Sounder.GetStatusHW")
        return self.parse_get_status_response(response)

    async def set_status(self, vid: int, status: Status) -> None:
        """Set the status of the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
            status: The status to set the keypad speaker to.
        """
        # INVOKE <id> Sounder.SetStatus <status (0/1/On/Off)>
        # -> R:INVOKE <id> <rcode> Sounder.SetStatus
        await self.invoke(vid, "Sounder.SetStatus", status)

    async def turn_on(self, vid: int) -> None:
        """Turn on the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
        """
        await self.set_status(vid, self.Status.ON)

    async def turn_off(self, vid: int) -> None:
        """Turn off the keypad speaker.

        Args:
            vid: The Vantage ID of the keypad.
        """
        await self.set_status(vid, self.Status.OFF)

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

    @classmethod
    def parse_get_frequency_response(cls, response: InterfaceResponse) -> Decimal:
        """Parse a 'Sounder.GetFrequency' response."""
        # -> R:INVOKE <id> <frequency> Sounder.GetFrequency
        return fixed_result(response)

    @classmethod
    def parse_get_status_response(cls, response: InterfaceResponse) -> Status:
        """Parse a 'Sounder.GetStatus' response."""
        # -> R:INVOKE <id> <status (0/1)> Sounder.GetStatus
        # -> S:STATUS <id> Sounder.GetStatus <status (0/1)>
        # -> EL: <id> Sounder.GetStatus <status (0/1)>
        return enum_result(cls.Status, response)
