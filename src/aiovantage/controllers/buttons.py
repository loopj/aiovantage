from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import Button

from .base import StatefulController


class ButtonsController(StatefulController[Button], ButtonInterface):
    # Fetch the following object types from Vantage
    vantage_types = ("Button",)

    # Get status updates from "STATUS BTN"
    status_types = ("BTN",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        pass  # Buttons are momentary, skip fetching initial state.

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a Button object.

        state: Dict[str, Any] = {}
        if status == "BTN":
            state["pressed"] = ButtonInterface.parse_btn_status(args)

        self.update_state(id, state)
