"""Controller holding and managing Vantage dry contacts."""

from typing_extensions import override

from aiovantage.command_client.object_interfaces import ButtonInterface
from aiovantage.models import DryContact

from .base import BaseController


class DryContactsController(BaseController[DryContact], ButtonInterface):
    """Controller holding and managing Vantage dry contacts."""

    vantage_types = ("DryContact",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("BTN",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a dry contact."""
        # Dry contacts are momentary, so default to not pressed to avoid a lookup
        state = {
            "triggered": False,
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "BTN":
            return

        # STATUS BTN
        # -> S:BTN <id> <state (PRESS/RELEASE)>
        state = {
            "triggered": args[0] == "PRESS",
        }

        self.update_state(vid, state)
