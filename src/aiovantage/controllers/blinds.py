from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import BlindInterface
from aiovantage.config_client.objects import Blind

from .base import StatefulController


class BlindsController(StatefulController[Blind], BlindInterface):
    # Fetch the following object types from Vantage
    vantage_types = ("QISBlind", "QubeBlind", "RelayBlind", "Somfy.URTSI_2_Shade_CHILD")

    # Subscribe to status updates from the event log for the following methods
    event_log_status = True
    event_log_status_methods = ("Blind.GetPosition",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Blind.

        state: Dict[str, Any] = {}
        state["position"] = await BlindInterface.get_position(self, id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a Blind.

        state: Dict[str, Any] = {}
        if status == "Blind.GetPosition":
            state["position"] = BlindInterface.parse_get_position_status(args)

        self.update_state(id, state)
