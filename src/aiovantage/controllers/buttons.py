"""Controller holding and managing Vantage buttons."""

from typing_extensions import override

from aiovantage.objects import Button

from .base import BaseController


class ButtonsController(BaseController[Button]):
    """Controller holding and managing Vantage buttons."""

    vantage_types = (Button,)
    status_types = ("BTN",)

    @override
    async def fetch_object_state(self, obj: Button) -> None:
        """Fetch the state properties of a dry contact."""
        state = {
            # Buttons are momentary, default to not pressed to avoid a lookup
            "state": Button.State.Up,
        }

        self.update_state(obj.id, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "BTN":
            return

        # STATUS BTN
        # -> S:BTN <id> <state (PRESS/RELEASE)>
        state = {
            "state": (Button.State.Down if args[0] == "PRESS" else Button.State.Up),
        }

        self.update_state(vid, state)
