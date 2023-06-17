"""Controller holding and managing Vantage dry contacts."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import DryContact

from .base import StatefulController


class DryContactsController(StatefulController[DryContact], ButtonInterface):
    """Controller holding and managing Vantage dry contacts."""

    # Fetch the following object types from Vantage
    vantage_types = ("DryContact",)

    # Get status updates from "STATUS BTN"
    status_types = ("BTN",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of a dry contact."""

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a dry contact."""

        state: Dict[str, Any] = {}
        if status == "BTN":
            state["triggered"] = ButtonInterface.parse_btn_status(args)

        self.update_state(vid, state)
