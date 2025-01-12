"""Controller holding and managing Vantage blinds."""

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
