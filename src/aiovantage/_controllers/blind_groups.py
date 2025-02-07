from aiovantage.controllers import BaseController
from aiovantage.objects import BlindGroup, SomfyRS485GroupChild, SomfyURTSI2GroupChild


class BlindGroupsController(
    BaseController[BlindGroup | SomfyRS485GroupChild | SomfyURTSI2GroupChild]
):
    """Blind groups controller."""

    vantage_types = (
        "BlindGroup",
        "Somfy.RS-485_Group_CHILD",
        "Somfy.URTSI_2_Group_CHILD",
    )
