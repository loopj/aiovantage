from aiovantage.aci_client.system_objects import RGBLoad
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController

# INVOKE <vid> RGBLoad.GetColor
#   -> R:INVOKE <vid> <color> RGBLoad.GetColor

# INVOKE <vid> RGBLoad.SetRGBW <red> <green> <blue> <white>
#   -> R:INVOKE <vid> <?> RGBLoad.SetRGBW <red> <green> <blue> <white>

# INVOKE <vid> RGBLoad.SetRGB <red> <green> <blue>
#   -> R:INVOKE <vid> <?> RGBLoad.SetRGB <red> <green> <blue>

# INVOKE <vid> RGBLoad.SetHSL <hue> <saturation> <level>
#   -> R:INVOKE <vid> <?> RGBLoad.SetHSL <hue> <saturation> <level>


class RGBLoadsController(BaseController[RGBLoad]):
    item_cls = RGBLoad
    vantage_types = (
        "Vantage.DGColorLoad",
        "Vantage.DDGColorLoad",
    )
    status_types = (StatusType.LOAD,)
