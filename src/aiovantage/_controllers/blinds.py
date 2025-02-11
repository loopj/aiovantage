from aiovantage.objects import (
    BlindGroup,
    QISBlind,
    QubeBlind,
    RelayBlind,
    SomfyRS485GroupChild,
    SomfyRS485ShadeChild,
    SomfyURTSI2GroupChild,
    SomfyURTSI2ShadeChild,
)

from .base import BaseController

BlindTypes = (
    BlindGroup
    | QISBlind
    | QubeBlind
    | RelayBlind
    | SomfyRS485GroupChild
    | SomfyRS485ShadeChild
    | SomfyURTSI2GroupChild
    | SomfyURTSI2ShadeChild
)
"""Types managed by the blinds controller."""


class BlindsController(BaseController[BlindTypes]):
    """Blinds controller."""

    vantage_types = (
        "BlindGroup",
        "QISBlind",
        "QubeBlind",
        "RelayBlind",
        "Somfy.URTSI_2_Group_CHILD",
        "Somfy.RS-485_Shade_CHILD",
        "Somfy.URTSI_2_Group_CHILD",
        "Somfy.URTSI_2_Shade_CHILD",
    )
