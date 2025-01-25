"""Controller holding and managing Vantage buttons."""

from typing_extensions import override

from aiovantage.objects import Button
from aiovantage.object_interfaces import ButtonInterface

from .base import BaseController


class ButtonsController(BaseController[Button], ButtonInterface):
    """Controller holding and managing Vantage buttons."""

    vantage_types = ("Button",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("BTN",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a dry contact."""
        state = {
            # Buttons are momentary, default to not pressed to avoid a lookup
            "pressed": False,
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
            "pressed": args[0] == "PRESS",
        }

        self.update_state(vid, state)
