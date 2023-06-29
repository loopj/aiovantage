"""Controller holding and managing Vantage buttons."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import Button

from .base import BaseController


class ButtonsController(BaseController[Button], ButtonInterface):
    """Controller holding and managing Vantage buttons."""

    # Fetch the following object types from Vantage
    vantage_types = ("Button",)

    # Get status updates from "STATUS BTN"
    status_types = ("BTN",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of a button."""

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a button."""

        state: Dict[str, Any] = {}
        if status == "BTN":
            state["pressed"] = ButtonInterface.parse_btn_status(args)

        self.update_state(vid, state)
