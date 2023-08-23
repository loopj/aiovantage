"""Interface for querying and controlling buttons."""

from enum import IntEnum
from typing import Sequence

from .base import Interface


class ButtonInterface(Interface):
    """Interface for querying and controlling buttons."""

    class State(IntEnum):
        """The state of the Button."""

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
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        response = await self.invoke(vid, "Button.GetState")
        state = self.State[response.args[1]]

        return state

    async def set_state(self, vid: int, state: State) -> None:
        """Set the state of a button.

        Args:
            vid: The Vantage ID of the button.
            state: The state to set the button to, either a State.Up or State.Down.
        """
        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> Button.SetState <state (Up/Down)>
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

    @classmethod
    def parse_get_state_status(cls, args: Sequence[str]) -> State:
        """Parse a 'Button.GetState' event.

        Args:
            args: The arguments of the event.

        Returns:
            The state of the button, either a State.UP or State.DOWN.
        """
        # ELLOG STATUS ON
        # -> EL: <id> Button.GetState <state (0/1)>
        # STATUS ADD <id>
        # -> S:STATUS <id> Button.GetState <state (0/1)>
        return cls.State(int(args[0]))
