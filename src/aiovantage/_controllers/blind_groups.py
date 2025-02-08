from aiovantage.objects import BlindGroup, SomfyRS485GroupChild, SomfyURTSI2GroupChild

from .base import BaseController


class BlindGroupsController(
    BaseController[BlindGroup | SomfyRS485GroupChild | SomfyURTSI2GroupChild]
):
    """Blind groups controller."""

    vantage_types = (
        "BlindGroup",
        "Somfy.RS-485_Group_CHILD",
        "Somfy.URTSI_2_Group_CHILD",
    )
