"""Controller holding and managing Vantage blinds."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import BlindInterface
from aiovantage.config_client.objects import Blind

from .base import BaseController, State


class BlindsController(BaseController[Blind], BlindInterface):
    """Controller holding and managing Vantage blinds."""

    # Fetch the following object types from Vantage
    vantage_types = (
        "QISBlind",
        "QubeBlind",
        "RelayBlind",
        "Somfy.RS-485_Shade_CHILD",
        "Somfy.URTSI_2_Shade_CHILD",
    )

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status = True
    enhanced_log_status_methods = ("Blind.GetPosition",)

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a blind."""
        return {
            "position": await BlindInterface.get_position(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a blind."""
        if status != "Blind.GetPosition":
            return None

        return {
            "position": BlindInterface.parse_get_position_status(args),
        }
