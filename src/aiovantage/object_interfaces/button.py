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
        "Button.GetHoldOn": Decimal,
        "Button.GetPolarity": Polarity,
        "Button.GetSndType": SndType,
        "Button.GetPlacement": int,
        "Button.GetPlacementHW": int,
        "Button.GetStateHW": State,
        "Button.GetHoldOnHW": Decimal,
        "Button.GetPolarityHW": Polarity,
        "Button.GetSndTypeHW": SndType,
    }

    # Status properties
    state: State | None = State.Up  # Button.GetState
    hold_on: Decimal | None = None  # Button.GetHoldOn
    polarity: Polarity | None = None  # Button.GetPolarity
    snd_type: SndType | None = None  # Button.GetSndType
    placement: int | None = None  # Button.GetPlacement

    # Methods
    async def get_state(self) -> State:
        """Get the state of a button.

        Returns:
            The pressed state of the button.
        """
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        return await self.invoke("Button.GetState")

    async def set_state(self, state: State) -> None:
        """Set the state of a button.

        Args:
            state: The state to set the button to, either a State.Up or State.Down.
        """
        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> <rcode> Button.SetState <state (Up/Down)>
        await self.invoke("Button.SetState", state)

    async def get_hold_on(self) -> Decimal:
        """Get the hold on time of a button.

        Returns:
            The hold on time of the button, in seconds.
        """
        # INVOKE <id> Button.GetHoldOn
        # -> R:INVOKE <id> <seconds> Button.GetHoldOn
        return await self.invoke("Button.GetHoldOn")

    async def set_hold_on(self, seconds: Decimal) -> None:
        """Set the hold on time of a button.

        Args:
            seconds: The hold on time to set, in seconds.
        """
        # INVOKE <id> <rcode> Button.SetHoldOn <seconds>
        # -> R:INVOKE <id> <rcode> Button.SetHoldOn <seconds>
        await self.invoke("Button.SetHoldOn", seconds)

    async def get_polarity(self) -> Polarity:
        """Get the polarity of a button.

        Returns:
            The polarity of the button.
        """
        # INVOKE <id> Button.GetPolarity
        # -> R:INVOKE <id> <polarity> Button.GetPolarity
        return await self.invoke("Button.GetPolarity")

    async def set_polarity(self, polarity: Polarity) -> None:
        """Set the polarity of a button.

        Args:
            polarity: The polarity to set the button to.
        """
        # INVOKE <id> Button.SetPolarity <polarity (0/1/NormallyOpen/NormallyClosed)>
        # -> R:INVOKE <id> <rcode> Button.SetPolarity <polarity (NormallyOpen/NormallyClosed)>
        await self.invoke("Button.SetPolarity", polarity)

    async def get_snd_type(self) -> SndType:
        """Get the sound type of a button.

        Returns:
            The sound type of the button.
        """
        # INVOKE <id> Button.GetSndType
        # -> R:INVOKE <id> <snd_type> Button.GetSndType
        return await self.invoke("Button.GetSndType")

    async def set_snd_type(self, snd_type: SndType) -> None:
        """Set the sound type of a button.

        Args:
            snd_type: The sound type to set the button to.
        """
        # INVOKE <id> Button.SetSndType <snd_type (0/1/2/Continuous/Pulsed/Off)>
        # -> R:INVOKE <id> <rcode> Button.SetSndType <snd_type (Continuous/Pulsed/Off)>
        await self.invoke("Button.SetSndType", snd_type)

    async def get_placement(self) -> int:
        """Get the placement of a button.

        Returns:
            The placement of the button on the keypad.
        """
        # INVOKE <id> Button.GetPlacement
        # -> R:INVOKE <id> <placement> Button.GetPlacement
        return await self.invoke("Button.GetPlacement")

    async def get_placement_hw(self) -> int:
        """Get the hardware placement of a button directly from the hardware.

        Returns:
            The placement of the button on the keypad.
        """
        # INVOKE <id> Button.GetPlacementHW
        # -> R:INVOKE <id> <placement> Button.GetPlacementHW
        return await self.invoke("Button.GetPlacementHW")

    async def set_placement(self, placement: int) -> None:
        """Set the placement of a button.

        Args:
            placement: The placement of the button on the keypad.
        """
        # INVOKE <id> Button.SetPlacement <placement>
        # -> R:INVOKE <id> <rcode> Button.SetPlacement <placement>
        await self.invoke("Button.SetPlacement", placement)

    async def get_state_hw(self) -> State:
        """Get the state of a button directly from the hardware.

        Returns:
            The pressed state of the button.
        """
        # INVOKE <id> Button.GetStateHW
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetStateHW
        return await self.invoke("Button.GetStateHW")

    async def set_state_sw(self, state: State) -> None:
        """Set the cached state of a button.

        Args:
            state: The state to set the button to.
        """
        # INVOKE <id> Button.SetStateSW <state (0/1/Up/Down)>
        # -> R:INVOKE <id> <rcode> Button.SetStateSW <state (Up/Down)>
        await self.invoke("Button.SetStateSW", state)

    async def get_hold_on_hw(self) -> Decimal:
        """Get the hold on time of a button directly from the hardware.

        Returns:
            The hold on time of the button, in seconds.
        """
        # INVOKE <id> Button.GetHoldOnHW
        # -> R:INVOKE <id> <seconds> Button.GetHoldOnHW
        return await self.invoke("Button.GetHoldOnHW")

    async def set_hold_on_sw(self, seconds: Decimal) -> None:
        """Set the cached hold on time of a button.

        Args:
            seconds: The hold on time to set, in seconds.
        """
        # INVOKE <id> Button.SetHoldOnSW <seconds>
        # -> R:INVOKE <id> <rcode> Button.SetHoldOnSW <seconds>
        await self.invoke("Button.SetHoldOnSW", seconds)

    async def get_polarity_hw(self) -> Polarity:
        """Get the polarity of a button directly from the hardware.

        Returns:
            The polarity of the button.
        """
        # INVOKE <id> Button.GetPolarityHW
        # -> R:INVOKE <id> <polarity> Button.GetPolarityHW
        return await self.invoke("Button.GetPolarityHW")

    async def set_polarity_sw(self, polarity: Polarity) -> None:
        """Set the cached polarity of a button.

        Args:
            polarity: The polarity to set the button to.
        """
        # INVOKE <id> Button.SetPolaritySW <polarity (0/1/NormallyOpen/NormallyClosed)>
        # -> R:INVOKE <id> <rcode> Button.SetPolaritySW <polarity (NormallyOpen/NormallyClosed)>
        await self.invoke("Button.SetPolaritySW", polarity)

    async def get_snd_type_hw(self) -> SndType:
        """Get the sound type of a button directly from the hardware.

        Returns:
            The sound type of the button.
        """
        # INVOKE <id> Button.GetSndTypeHW
        # -> R:INVOKE <id> <snd_type> Button.GetSndTypeHW
        return await self.invoke("Button.GetSndTypeHW")

    async def set_snd_type_sw(self, snd_type: SndType) -> None:
        """Set the cached sound type of a button.

        Args:
            snd_type: The sound type to set the button to.
        """
        # INVOKE <id> Button.SetSndTypeSW <snd_type (0/1/2/Continuous/Pulsed/Off)>
        # -> R:INVOKE <id> <rcode> Button.SetSndTypeSW <snd_type (Continuous/Pulsed/Off)>
        await self.invoke("Button.SetSndTypeSW", snd_type)

    async def set_placement_sw(self, placement: int) -> None:
        """Set the cached placement of a button.

        Args:
            placement: The placement of the button on the keypad.
        """
        # INVOKE <id> Button.SetPlacementSW <placement>
        # -> R:INVOKE <id> <rcode> Button.SetPlacementSW <placement>
        await self.invoke("Button.SetPlacementSW", placement)

    # Additional convenience methods, not part of the Vantage API
    async def press(self) -> None:
        """Press a button."""
        await self.set_state(self.State.Down)

    async def release(self) -> None:
        """Release a button."""
        await self.set_state(self.State.Up)

    async def press_and_release(self) -> None:
        """Press and release a button."""
        await self.press()
        await self.release()
