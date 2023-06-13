from typing import Sequence

from .base import Interface


class ButtonInterface(Interface):
    async def get_state(self, id: int) -> bool:
        """
        Get the state of a button.

        Args:
            id: The ID of the button.

        Returns:
            The pressed state of the button, True if pressed, False if not.
        """

        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        response = await self.invoke(id, "Button.GetState")
        state = response.args[1]
        if state == "Up":
            return False
        elif state == "Down":
            return True
        else:
            raise ValueError(f"Invalid button state name: {state}")

    async def set_state(self, id: int, pressed: bool) -> None:
        """
        Set the state of a button.

        Args:
            id: The ID of the button.
            state: The state to set the button to, either a State.UP or State.DOWN.
        """

        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> Button.SetState <state (Up/Down)>
        await self.invoke(id, "Button.SetState", pressed)

    async def press(self, id: int) -> None:
        """
        Press a button.

        Args:
            id: The ID of the button.
        """

        await self.set_state(id, True)

    async def release(self, id: int) -> None:
        """
        Release a button.

        Args:
            id: The ID of the button.
        """

        await self.set_state(id, False)

    async def press_and_release(self, id: int) -> None:
        """
        Press and release a button.

        Args:
            id: The ID of the button.
        """

        await self.press(id)
        await self.release(id)

    @classmethod
    def parse_btn_status(cls, args: Sequence[str]) -> bool:
        """
        Parse a simple "S:BTN" event.

        Args:
            args: The arguments of the event.

        Returns:
            The state of the button, either a State.UP or State.DOWN.
        """

        # STATUS BTN
        # -> S:BTN <id> <state (PRESS/RELEASE)>
        state = args[0]
        if state == "RELEASE":
            return False
        elif state == "PRESS":
            return True
        else:
            raise ValueError(f"Invalid button state name: {state}")

    @classmethod
    def parse_get_state_status(cls, args: Sequence[str]) -> bool:
        """
        Parse a "Button.GetState" event.

        Args:
            args: The arguments of the event.

        Returns:
            The state of the button, either a State.UP or State.DOWN.
        """

        # ELLOG STATUS ON
        # -> EL: <id> Button.GetState <state (0/1)>

        # STATUS ADD <id>
        # -> S:STATUS <id> Button.GetState <state (0/1)>
        return bool(int(args[0]))
