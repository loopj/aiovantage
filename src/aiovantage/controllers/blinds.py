"""Controller holding and managing Vantage blinds."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import (
    QISBlind,
    QubeBlind,
    RelayBlind,
    SomfyRS485ShadeChild,
    SomfyURTSI2ShadeChild,
)

from .base import BaseController

# The various "blind" object types don't all inherit from the same base class,
# so for typing purposes we'll use a union of all the types.
BlindTypes = (
    QISBlind | QubeBlind | RelayBlind | SomfyRS485ShadeChild | SomfyURTSI2ShadeChild
)


class BlindsController(BaseController[BlindTypes]):
    """Controller holding and managing Vantage blinds."""

    vantage_types = (
        QISBlind,
        QubeBlind,
        RelayBlind,
        SomfyRS485ShadeChild,
        SomfyURTSI2ShadeChild,
    )
    status_types = ("BLIND",)
    fetch_properties = ("position",)

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
