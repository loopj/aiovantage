"""Interface for querying and controlling buttons."""

from enum import IntEnum

from .base import Interface, InterfaceResponse, enum_result


class ButtonInterface(Interface):
    """Interface for querying and controlling buttons."""

    class State(IntEnum):
        """Button state."""

        UP = 0
        DOWN = 1

    async def get_state(self, vid: int) -> State:
        """Get the state of a button.

        Args:
            vid: The Vantage ID of the button.

        Returns:
            The pressed state of the button, True if pressed, False if not.
        """
        # INVOKE <id> Button.GetState
        response = await self.invoke(vid, "Button.GetState")
        return self.parse_get_state_response(response)

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
        await self.set_state(vid, self.State.DOWN)

    async def release(self, vid: int) -> None:
        """Release a button.

        Args:
            vid: The Vantage ID of the button.
        """
        await self.set_state(vid, self.State.UP)

    async def press_and_release(self, vid: int) -> None:
        """Press and release a button.

        Args:
            vid: The Vantage ID of the button.
        """
        await self.press(vid)
        await self.release(vid)

    @classmethod
    def parse_get_state_response(cls, response: InterfaceResponse) -> State:
        """Parse a 'Button.GetState' response."""
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        # -> S:STATUS <id> Button.GetState <state (0/1)>
        # -> EL: <id> Button.GetState <state (0/1)>
        return enum_result(cls.State, response)
