"""Controller holding and managing Vantage dry contacts."""

from typing_extensions import override

from aiovantage.objects import DryContact

from .base import BaseController


class DryContactsController(BaseController[DryContact]):
    """Controller holding and managing Vantage dry contacts."""

    vantage_types = (DryContact,)
    status_types = ("BTN",)

    @override
    async def fetch_object_state(self, obj: DryContact) -> None:
        """Fetch the state properties of a dry contact."""
        # Dry contacts are momentary, so default to not pressed to avoid a lookup
        state = {
            "state": DryContact.State.Up,
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
            "state": (
                DryContact.State.Down if args[0] == "PRESS" else DryContact.State.Up
            ),
        }

        self.update_state(vid, state)
