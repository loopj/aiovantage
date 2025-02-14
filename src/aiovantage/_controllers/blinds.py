from aiovantage.objects import (
    BlindGroup,
    QISBlind,
    QubeBlind,
    RelayBlind,
    SomfyRS485ShadeChild,
    SomfyURTSI2ShadeChild,
)

from .base import Controller
from .query import QuerySet

BlindTypes = (
    QISBlind | QubeBlind | RelayBlind | SomfyRS485ShadeChild | SomfyURTSI2ShadeChild
)
"""Types managed by the blinds controller."""


class BlindsController(Controller[BlindTypes]):
    """Blinds controller."""

    vantage_types = (
        "QISBlind",
        "QubeBlind",
        "RelayBlind",
        "Somfy.RS-485_Shade_CHILD",
        "Somfy.URTSI_2_Shade_CHILD",
    )

    def in_blind_group(self, blind_group: BlindGroup) -> QuerySet[BlindTypes]:
        """Return a queryset of all loads in the given blind group."""
        return self.filter(lambda load: load.vid in blind_group.blind_table)
