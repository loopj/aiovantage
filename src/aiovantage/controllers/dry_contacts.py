"""Controller holding and managing Vantage dry contacts."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import ButtonInterface
from aiovantage.models import DryContact

from .base import BaseController, State


class DryContactsController(BaseController[DryContact], ButtonInterface):
    """Controller holding and managing Vantage dry contacts."""

    vantage_types = ("DryContact",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("BTN",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, _vid: int) -> State:
        """Fetch the state properties of a dry contact."""
        return {
            # Dry contacts are momentary, so default to not pressed to avoid a lookup
            "triggered": False,
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a dry contact."""
        if status != "BTN":
            return None

        # STATUS BTN
        # -> S:BTN <id> <state (PRESS/RELEASE)>
        return {
            "triggered": args[0] == "PRESS",
        }
