"""Controller holding and managing Vantage blinds."""

from aiovantage.objects import (
    BlindGroup,
    QISBlind,
    QubeBlind,
    RelayBlind,
    SomfyRS485ShadeChild,
    SomfyURTSI2ShadeChild,
)

from .base import BaseController

BlindTypes = (
    BlindGroup
    | QISBlind
    | QubeBlind
    | RelayBlind
    | SomfyRS485ShadeChild
    | SomfyURTSI2ShadeChild
)


class BlindsController(BaseController[BlindTypes]):
    """Controller holding and managing Vantage blinds."""

    vantage_types = (
        BlindGroup,
        QISBlind,
        QubeBlind,
        RelayBlind,
        SomfyRS485ShadeChild,
        SomfyURTSI2ShadeChild,
    )
