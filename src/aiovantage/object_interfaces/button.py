"""Interface for querying and controlling buttons."""

from enum import IntEnum

from .base import Interface


class ButtonInterface(Interface):
    """Interface for querying and controlling buttons."""

    class State(IntEnum):
        """Button state."""

        Up = 0
        Down = 1

    method_signatures = {
        "Button.GetState": State,
    }

    # Properties
    state: State | None = None  # not part of the interface, just for convenience

    # Methods
    async def get_state(self) -> State:
        """Get the state of a button.

        Returns:
            The pressed state of the button, True if pressed, False if not.
        """
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        return await self.invoke("Button.GetState", as_type=ButtonInterface.State)

    async def set_state(self, state: State) -> None:
        """Set the state of a button.

        Args:
            state: The state to set the button to, either a State.Up or State.Down.
        """
        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> <rcode> Button.SetState <state (Up/Down)>
        await self.invoke("Button.SetState", state)

    # Additional convenience methods, not part of the Vantage API
    async def press(self) -> None:
        """Press a button."""
        await self.set_state(ButtonInterface.State.Down)

    async def release(self) -> None:
        """Release a button."""
        await self.set_state(ButtonInterface.State.Up)

    async def press_and_release(self) -> None:
        """Press and release a button."""
        await self.press()
        await self.release()
