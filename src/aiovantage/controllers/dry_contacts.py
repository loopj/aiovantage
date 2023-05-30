from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import ButtonInterface
from aiovantage.config_client.objects import DryContact

from .base import StatefulController


class DryContactsController(StatefulController[DryContact], ButtonInterface):
    # Store objects managed by this controller as DryContact instances
    item_cls = DryContact

    # Fetch DryContact objects from Vantage
    vantage_types = (DryContact,)

    # Subscribe to status updates from the event log for the following methods
    event_log_status_methods = ("Button.GetState",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        # DryContacts are momentary, fetching initial state is not worth the overhead.
        pass

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a DryContact object.

        state: Dict[str, Any] = {}
        if status == "Button.GetState":
            # <id> Button.GetState <state (0/1)>
            state["state"] = DryContact.State(int(args[0]))

        self.update_state(id, state)
