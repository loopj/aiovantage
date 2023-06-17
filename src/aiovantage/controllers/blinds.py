"""Controller holding and managing Vantage blinds."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import BlindInterface
from aiovantage.config_client.objects import Blind

from .base import StatefulController


class BlindsController(StatefulController[Blind], BlindInterface):
    """Controller holding and managing Vantage blinds."""

    # Fetch the following object types from Vantage
    vantage_types = ("QISBlind", "QubeBlind", "RelayBlind", "Somfy.URTSI_2_Shade_CHILD")

    # Subscribe to status updates from the event log for the following methods
    event_log_status = True
    event_log_status_methods = ("Blind.GetPosition",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of a blind."""

        state: Dict[str, Any] = {}
        state["position"] = await BlindInterface.get_position(self, vid)

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a blind."""

        state: Dict[str, Any] = {}
        if status == "Blind.GetPosition":
            state["position"] = BlindInterface.parse_get_position_status(args)

        self.update_state(vid, state)
