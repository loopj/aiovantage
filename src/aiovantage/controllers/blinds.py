"""Controller holding and managing Vantage blinds."""

from aiovantage.objects import (
    Blind,
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
    Blind
    | BlindGroup
    | QISBlind
    | QubeBlind
    | RelayBlind
    | SomfyRS485GroupChild
    | SomfyRS485ShadeChild
    | SomfyURTSI2GroupChild
    | SomfyURTSI2ShadeChild
)


class BlindsController(BaseController[BlindTypes]):
    """Controller holding and managing Vantage blinds."""

    vantage_types = (
        Blind,
        BlindGroup,
        QISBlind,
        QubeBlind,
        RelayBlind,
        SomfyRS485GroupChild,
        SomfyRS485ShadeChild,
        SomfyURTSI2GroupChild,
        SomfyURTSI2ShadeChild,
    )
