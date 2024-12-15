"""Controller holding and managing Vantage blinds."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.controllers.base import BaseController
from aiovantage.objects import (
    QISBlind,
    QubeBlind,
    RelayBlind,
    SomfyRS485ShadeChild,
    SomfyURTSI2ShadeChild,
)

# The various "blind" object types don't all inherit from the same base class,
# so for typing purposes we'll export a union of all the types.

BlindTypes = (
    QISBlind | QubeBlind | RelayBlind | SomfyRS485ShadeChild | SomfyURTSI2ShadeChild
)
"""Types of objects that are considered 'blinds'."""


class BlindsController(BaseController[BlindTypes]):
    """Controller holding and managing Vantage blinds."""

    vantage_types = (
        "QISBlind",
        "QubeBlind",
        "RelayBlind",
        "Somfy.RS-485_Shade_CHILD",
        "Somfy.URTSI_2_Shade_CHILD",
    )

    status_types = ("BLIND",)

    @override
    async def fetch_object_state(self, obj: BlindTypes) -> None:
        """Fetch the state properties of a blind."""
        state = {
            "position": await obj.get_position(),
        }

        self.update_state(obj.id, state)

    @override
    def handle_simple_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "BLIND":
            return

        # STATUS BLIND
        # -> S:BLIND <id> <position (0.000 - 100.000)>
        state = {
            "position": Decimal(args[0]),
        }

        self.update_state(vid, state)
