from ..clients.hc import StatusType
from ..models.button import Button
from .base import BaseController


class ButtonsController(BaseController[Button]):
    item_cls = Button
    vantage_types = ("Button",)
    status_types = (StatusType.BTN,)
