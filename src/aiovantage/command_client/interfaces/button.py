from enum import Enum

from .base import Interface


class ButtonInterface(Interface):
    class State(Enum):
        UP = 0
        DOWN = 1

    async def get_state(self, id: int) -> State:
        """
        Get the state of a button.

        Args:
            id: The ID of the button.

        Returns:
            The state of the button, either a State.UP or State.DOWN.
        """
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        response = await self.invoke(id, "Button.GetState")
        state = response.args[1]

        return self._state_from_name(state)

    async def set_state(self, id: int, state: State) -> None:
        """
        Set the state of a button.

        Args:
            id: The ID of the button.
            state: The state to set the button to, either a State.UP or State.DOWN.
        """

        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> Button.SetState <state (Up/Down)>
        await self.invoke(id, "Button.SetState", state.value)

    async def press(self, id: int) -> None:
        """
        Press a button.

        Args:
            id: The ID of the button.
        """

        await self.set_state(id, self.State.DOWN)

    async def release(self, id: int) -> None:
        """
        Release a button.

        Args:
            id: The ID of the button.
        """

        await self.set_state(id, self.State.UP)

    async def press_and_release(self, id: int) -> None:
        """
        Press and release a button.

        Args:
            id: The ID of the button.
        """

        await self.press(id)
        await self.release(id)

    def _state_from_name(self, name: str) -> State:
        if name == "Up":
            return self.State.UP
        elif name == "Down":
            return self.State.DOWN
        else:
            raise ValueError(f"Invalid button state name: {name}")
