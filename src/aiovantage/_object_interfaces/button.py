from decimal import Decimal
from enum import IntEnum

from typing_extensions import override

from .base import Interface, method


class ButtonInterface(Interface):
    """Button object interface."""

    interface_name = "Button"

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

    # Properties
    state: State | None = State.Up

    # Methods
    @method("GetState", "GetStateHW", property="state")
    async def get_state(self, *, hw: bool = False) -> State:
        """Get the state of a button.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The pressed state of the button.
        """
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        return await self.invoke("Button.GetStateHW" if hw else "Button.GetState")

    @method("SetState", "SetStateSW")
    async def set_state(self, state: State, *, sw: bool = False) -> None:
        """Set the state of a button.

        Args:
            state: The state to set the button to, either a State.UP or State.DOWN.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> <rcode> Button.SetState <state (Up/Down)>
        await self.invoke("Button.SetStateSW" if sw else "Button.SetState", state)

    @method("GetHoldOn", "GetHoldOnHW")
    async def get_hold_on(self, *, hw: bool = False) -> Decimal:
        """Get the hold on time of a button.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The hold on time of the button, in seconds.
        """
        # INVOKE <id> Button.GetHoldOn
        # -> R:INVOKE <id> <seconds> Button.GetHoldOn
        return await self.invoke("Button.GetHoldOnHW" if hw else "Button.GetHoldOn")

    @method("SetHoldOn", "SetHoldOnSW")
    async def set_hold_on(self, seconds: Decimal, *, sw: bool = False) -> None:
        """Set the hold on time of a button.

        Args:
            seconds: The hold on time to set, in seconds.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetHoldOn <seconds>
        # -> R:INVOKE <id> <rcode> Button.SetHoldOn <seconds>
        await self.invoke("Button.SetHoldOnSW" if sw else "Button.SetHoldOn", seconds)

    @method("GetPolarity", "GetPolarityHW")
    async def get_polarity(self, *, hw: bool = False) -> Polarity:
        """Get the polarity of a button.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The polarity of the button.
        """
        # INVOKE <id> Button.GetPolarity
        # -> R:INVOKE <id> <polarity> Button.GetPolarity
        return await self.invoke("Button.GetPolarityHW" if hw else "Button.GetPolarity")

    @method("SetPolarity", "SetPolaritySW")
    async def set_polarity(self, polarity: Polarity, *, sw: bool = False) -> None:
        """Set the polarity of a button.

        Args:
            polarity: The polarity to set the button to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetPolarity <polarity (0/1/NormallyOpen/NormallyClosed)>
        # -> R:INVOKE <id> <rcode> Button.SetPolarity <polarity (NormallyOpen/NormallyClosed)>
        await self.invoke(
            "Button.SetPolaritySW" if sw else "Button.SetPolarity", polarity
        )

    @method("GetSndType", "GetSndTypeHW")
    async def get_snd_type(self, *, hw: bool = False) -> SndType:
        """Get the sound type of a button.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The sound type of the button.
        """
        # INVOKE <id> Button.GetSndType
        # -> R:INVOKE <id> <snd_type> Button.GetSndType
        return await self.invoke("Button.GetSndTypeHW" if hw else "Button.GetSndType")

    @method("SetSndType", "SetSndTypeSW")
    async def set_snd_type(self, snd_type: SndType, *, sw: bool = False) -> None:
        """Set the sound type of a button.

        Args:
            snd_type: The sound type to set the button to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetSndType <snd_type (0/1/2/Continuous/Pulsed/Off)>
        # -> R:INVOKE <id> <rcode> Button.SetSndType <snd_type (Continuous/Pulsed/Off)>
        await self.invoke(
            "Button.SetSndTypeSW" if sw else "Button.SetSndType", snd_type
        )

    @method("GetPlacement", "GetPlacementHW")
    async def get_placement(self, *, hw: bool = False) -> int:
        """Get the placement of a button.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The placement of the button on the keypad.
        """
        # INVOKE <id> Button.GetPlacement
        # -> R:INVOKE <id> <placement> Button.GetPlacement
        return await self.invoke(
            "Button.GetPlacementHW" if hw else "Button.GetPlacement"
        )

    @method("SetPlacement", "SetPlacementSW")
    async def set_placement(self, placement: int, *, sw: bool = False) -> None:
        """Set the placement of a button.

        Args:
            placement: The placement of the button on the keypad.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> Button.SetPlacement <placement>
        # -> R:INVOKE <id> <rcode> Button.SetPlacement <placement>
        await self.invoke(
            "Button.SetPlacementSW" if sw else "Button.SetPlacement", placement
        )

    # Convenience functions, not part of the interface
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

    @property
    def is_down(self) -> bool | None:
        """Return True if the button is down."""
        return self.state == self.State.Down

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "BTN":
            # STATUS BTN
            # -> S:BTN <id> <state (PRESS/RELEASE)>
            btn_map = {
                "PRESS": ButtonInterface.State.Down,
                "RELEASE": ButtonInterface.State.Up,
            }

            return self.update_properties({"state": btn_map[args[0]]})

        return super().handle_category_status(category, *args)
