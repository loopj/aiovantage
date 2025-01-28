"""Controller holding and managing Vantage buttons."""

from typing_extensions import override

from aiovantage.objects import Button

from .base import BaseController


class ButtonsController(BaseController[Button]):
    """Controller holding and managing Vantage buttons."""

    vantage_types = ("Button",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("BTN",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    def handle_status(self, obj: Button, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "BTN":
            return

        # STATUS BTN
        # -> S:BTN <id> <state (PRESS/RELEASE)>
        state = {
            "state": Button.State.Down if args[0] == "PRESS" else Button.State.Up,
        }

        self.update_state(obj, state)
