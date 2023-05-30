from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import Button

from .base import StatefulController


class ButtonsController(StatefulController[Button], ButtonInterface):
    # Store objects managed by this controller as Load instances
    item_cls = Button

    # Fetch Load objects from Vantage
    vantage_types = (Button,)

    # Subscribe to status updates from the event log for the following methods
    event_log_status_methods = ("Button.GetState",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        pass # Buttons are momentary, fetching initial state is not worth the overhead.

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a Button object.

        state: Dict[str, Any] = {}
        if status == "Button.GetState":
            # <id> Button.GetState <state (0/1)>
            state["state"] = Button.State(int(args[0]))

        self.update_state(id, state)
