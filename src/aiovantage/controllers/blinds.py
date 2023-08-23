"""Controller holding and managing Vantage blinds."""

from decimal import Decimal
from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import BlindInterface
from aiovantage.models import BlindBase

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

    status_types = ("BLIND",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a blind."""
        return {
            "position": await BlindInterface.get_position(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a blind."""
        if status != "BLIND":
            return None

        # STATUS BLIND
        # -> S:BLIND <id> <position (0.000 - 100.000)>
        return {
            "position": Decimal(args[0]),
        }
