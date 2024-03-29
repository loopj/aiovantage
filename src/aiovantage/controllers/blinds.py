"""Controller holding and managing Vantage blinds."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.command_client.object_interfaces import BlindInterface
from aiovantage.models import BlindBase

from .base import BaseController


class BlindsController(BaseController[BlindBase], BlindInterface):
    """Controller holding and managing Vantage blinds."""

    vantage_types = (
        "QISBlind",
        "QubeBlind",
        "RelayBlind",
        "Somfy.RS-485_Shade_CHILD",
        "Somfy.URTSI_2_Shade_CHILD",
    )
    """The Vantage object types that this controller will fetch."""

    status_types = ("BLIND",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a blind."""
        state = {
            "position": await BlindInterface.get_position(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "BLIND":
            return

        # STATUS BLIND
        # -> S:BLIND <id> <position (0.000 - 100.000)>
        state = {
            "position": Decimal(args[0]),
        }

        self.update_state(vid, state)
