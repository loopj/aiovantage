"""Controller holding and managing Vantage blinds."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import BlindInterface
from aiovantage.config_client.models import BlindBase

from .base import BaseController, State


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

    enhanced_log_status_methods = ("Blind.GetPosition",)
    """Which status methods this controller handles from the Enhanced Log."""

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
