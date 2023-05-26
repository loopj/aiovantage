from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Button
from aiovantage.controllers.base import StatefulController
from aiovantage.query import QuerySet


class ButtonsController(StatefulController[Button]):
    # Store objects managed by this controller as Load instances
    item_cls = Button

    # Fetch Load objects from Vantage
    vantage_types = (Button,)

    # Get status updates from the event log
    event_log_status = True

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Button.

        # Buttons are momentary, so fetching initial state is not worth the overhead.
        pass

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a Button object.

        state: Dict[str, Any] = {}
        if status == "Button.GetState":
            # <id> Button.GetState <state (0/1)>
            state["state"] = Button.State(int(args[0]))

        self.update_state(id, state)

    @property
    def with_tasks(self) -> QuerySet[Button]:
        """
        Return a queryset of buttons that have tasks assigned to them.
        """

        return self.filter(lambda button: button.has_task)

    async def get_state(self, id: int) -> Button.State:
        """
        Get the state of a button.

        Args:
            id: The ID of the button.

        Returns:
            The state of the button, either a State.UP or State.DOWN.
        """
        # INVOKE <id> Button.GetState
        # -> R:INVOKE <id> <state (Up/Down)> Button.GetState
        response = await self.command_client.command("INVOKE", id, "Button.GetState")
        state = response.args[1]

        return self._state_from_name(state)

    async def set_state(self, id: int, state: Button.State) -> None:
        """
        Set the state of a button.

        Args:
            id: The ID of the button.
            state: The state to set the button to, either a State.UP or State.DOWN.
        """

        # INVOKE <id> Button.SetState <state (0/1/Up/Down)>
        # -> R:INVOKE <id> Button.SetState <state (Up/Down)>
        await self.command_client.command("INVOKE", id, "Button.SetState", state.value)

    async def press(self, id: int) -> None:
        """
        Press a button.

        Args:
            id: The ID of the button.
        """

        await self.set_state(id, Button.State.DOWN)

    async def release(self, id: int) -> None:
        """
        Release a button.

        Args:
            id: The ID of the button.
        """

        await self.set_state(id, Button.State.UP)

    async def press_and_release(self, id: int) -> None:
        """
        Press and release a button.

        Args:
            id: The ID of the button.
        """

        await self.press(id)
        await self.release(id)

    def _state_from_name(self, name: str) -> Button.State:
        if name == "Up":
            return Button.State.UP
        elif name == "Down":
            return Button.State.DOWN
        else:
            raise ValueError(f"Invalid button state name: {name}")