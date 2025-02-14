from aiovantage.objects import BlindGroup, SomfyRS485GroupChild, SomfyURTSI2GroupChild

from .base import Controller

BlindGroupTypes = BlindGroup | SomfyRS485GroupChild | SomfyURTSI2GroupChild
"""Types managed by the blind groups controller."""


class BlindGroupsController(Controller[BlindGroupTypes]):
    """Blind groups controller."""

    vantage_types = (
        "BlindGroup",
        "Somfy.RS-485_Group_CHILD",
        "Somfy.URTSI_2_Group_CHILD",
    )
