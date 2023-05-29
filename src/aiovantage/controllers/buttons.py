from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Button

from .base import StatefulController
from .interfaces.button import ButtonInterface


class ButtonsController(StatefulController[Button], ButtonInterface):
    # Store objects managed by this controller as Load instances
    item_cls = Button

    # Fetch Load objects from Vantage
    vantage_types = (Button,)

    # Get status updates from the event log
    event_log_status = True

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Buttons are momentary, fetching initial state is not worth the overhead.
        pass

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a Button object.

        state: Dict[str, Any] = {}
        if status == "Button.GetState":
            # <id> Button.GetState <state (0/1)>
            state["state"] = Button.State(int(args[0]))

        self.update_state(id, state)
