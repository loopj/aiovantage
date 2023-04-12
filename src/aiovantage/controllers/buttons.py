from aiovantage.aci_client.system_objects import Button
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType


class ButtonsController(BaseController[Button]):
    item_cls = Button
    vantage_types = ("Button",)
    status_types = (StatusType.BTN,)
