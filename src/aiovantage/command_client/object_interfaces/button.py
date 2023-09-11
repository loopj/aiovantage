"""Interface for querying and controlling buttons."""

from enum import IntEnum

from .base import Interface
from .parsers import parse_enum


class ButtonInterface(Interface):
    """Interface for querying and controlling buttons."""

    response_parsers = {
        "Button.GetState": lambda r: parse_enum(ButtonInterface.State, r),
    }

    class State(IntEnum):
        """Button state."""

        Up = 0
        Down = 1

    async def get_state(self, vid: int) -> State:
        """Get the state of a button.

        Args:
            vid: The Vantage ID of the button.

        Returns:
            The pressed state of the button, True if pressed, False if not.
        """
        # INVOKE <id> Button.GetState
        response = await self.invoke(vid, "Button.GetState")
        return ButtonInterface.parse_response(response, self.State)

    async def set_state(self, vid: int, state: State) -> None:
        """Set the state of a button.

        Args:
            vid: The Vantage ID of the button.
            state: The state to set the button to, either a State.Up or State.Down.
        """
        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> <rcode> Button.SetState <state (Up/Down)>
        await self.invoke(vid, "Button.SetState", state)

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
