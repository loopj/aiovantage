"""Interface for querying and controlling buttons."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class ButtonInterface(Interface):
    """Interface for querying and controlling buttons."""

    class State(IntEnum):
        """Button state."""

        Up = 0
        Down = 1

    class SndType(IntEnum):
        """Button sound type."""

        Continuous = 0
        Pulsed = 1
        Off = 2

    class Polarity(IntEnum):
        """Button polarity."""

        NormallyOpen = 0
        NormallyClosed = 1

    method_signatures = {
        "Button.GetState": State,
        "Button.GetStateHW": State,
        "Button.GetHoldOn": Decimal,
        "Button.GetHoldOnHW": Decimal,
        "Button.GetPolarity": Polarity,
        "Button.GetPolarityHW": Polarity,
        "Button.GetSndType": SndType,
        "Button.GetSndTypeHW": SndType,
        "Button.GetPlacement": int,
        "Button.GetPlacementHW": int,
    }

    async def get_state(self, vid: int, *, hw: bool = False) -> State:
        """Get the state of a button.

        Args:
            vid: The Vantage ID of the button.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The pressed state of the button.
        """
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        return await self.invoke(vid, "Button.GetStateHW" if hw else "Button.GetState")

    async def set_state(self, vid: int, state: State, *, sw: bool = False) -> None:
        """Set the state of a button.

        Args:
            vid: The Vantage ID of the button.
            state: The state to set the button to, either a State.UP or State.DOWN.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> <rcode> Button.SetState <state (Up/Down)>
        await self.invoke(vid, "Button.SetStateSW" if sw else "Button.SetState", state)

    async def get_hold_on(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the hold on time of a button.

        Args:
            vid: The Vantage ID of the button.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The hold on time of the button, in seconds.
        """
        # INVOKE <id> Button.GetHoldOn
        # -> R:INVOKE <id> <seconds> Button.GetHoldOn
        return await self.invoke(
            vid, "Button.GetHoldOnHW" if hw else "Button.GetHoldOn"
        )

    async def set_hold_on(
        self, vid: int, seconds: Decimal, *, sw: bool = False
    ) -> None:
        """Set the hold on time of a button.

        Args:
            vid: The Vantage ID of the button.
            seconds: The hold on time to set, in seconds.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetHoldOn <seconds>
        # -> R:INVOKE <id> <rcode> Button.SetHoldOn <seconds>
        await self.invoke(
            vid, "Button.SetHoldOnSW" if sw else "Button.SetHoldOn", seconds
        )

    async def get_polarity(self, vid: int, *, hw: bool = False) -> Polarity:
        """Get the polarity of a button.

        Args:
            vid: The Vantage ID of the button.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The polarity of the button.
        """
        # INVOKE <id> Button.GetPolarity
        # -> R:INVOKE <id> <polarity> Button.GetPolarity
        return await self.invoke(
            vid, "Button.GetPolarityHW" if hw else "Button.GetPolarity"
        )

    async def set_polarity(
        self, vid: int, polarity: Polarity, *, sw: bool = False
    ) -> None:
        """Set the polarity of a button.

        Args:
            vid: The Vantage ID of the button.
            polarity: The polarity to set the button to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetPolarity <polarity (0/1/NormallyOpen/NormallyClosed)>
        # -> R:INVOKE <id> <rcode> Button.SetPolarity <polarity (NormallyOpen/NormallyClosed)>
        await self.invoke(
            vid, "Button.SetPolaritySW" if sw else "Button.SetPolarity", polarity
        )

    async def get_snd_type(self, vid: int, *, hw: bool = False) -> SndType:
        """Get the sound type of a button.

        Args:
            vid: The Vantage ID of the button.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The sound type of the button.
        """
        # INVOKE <id> Button.GetSndType
        # -> R:INVOKE <id> <snd_type> Button.GetSndType
        return await self.invoke(
            vid, "Button.GetSndTypeHW" if hw else "Button.GetSndType"
        )

    async def set_snd_type(
        self, vid: int, snd_type: SndType, *, sw: bool = False
    ) -> None:
        """Set the sound type of a button.

        Args:
            vid: The Vantage ID of the button.
            snd_type: The sound type to set the button to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetSndType <snd_type (0/1/2/Continuous/Pulsed/Off)>
        # -> R:INVOKE <id> <rcode> Button.SetSndType <snd_type (Continuous/Pulsed/Off)>
        await self.invoke(
            vid, "Button.SetSndTypeSW" if sw else "Button.SetSndType", snd_type
        )

    async def get_placement(self, vid: int, *, hw: bool = False) -> int:
        """Get the placement of a button.

        Args:
            vid: The Vantage ID of the button.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The placement of the button on the keypad.
        """
        # INVOKE <id> Button.GetPlacement
        # -> R:INVOKE <id> <placement> Button.GetPlacement
        return await self.invoke(
            vid, "Button.GetPlacementHW" if hw else "Button.GetPlacement"
        )

    async def set_placement(
        self, vid: int, placement: int, *, sw: bool = False
    ) -> None:
        """Set the placement of a button.

        Args:
            vid: The Vantage ID of the button.
            placement: The placement of the button on the keypad.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetPlacement <placement>
        # -> R:INVOKE <id> <rcode> Button.SetPlacement <placement>
        await self.invoke(
            vid, "Button.SetPlacementSW" if sw else "Button.SetPlacement", placement
        )

    # Convenience functions, not part of the interface
    async def press(self, vid: int) -> None:
        """Press a button.

        Args:
            vid: The Vantage ID of the button.
        """
        await self.set_state(vid, self.State.Down)

    async def release(self, vid: int) -> None:
        """Release a button.

        Args:
            vid: The Vantage ID of the button.
        """
        await self.set_state(vid, self.State.Up)

    async def press_and_release(self, vid: int) -> None:
        """Press and release a button.

        Args:
            vid: The Vantage ID of the button.
        """
        await self.press(vid)
        await self.release(vid)
