from aiovantage.hc_client import StatusType
from aiovantage.controllers.base import BaseController
from aiovantage.models.button import Button


class ButtonsController(BaseController[Button]):
    item_cls = Button
    vantage_types = ("Button",)
    status_types = (StatusType.BTN,)
