from ..models.button import Button
from .base import BaseController


class ButtonsController(BaseController[Button]):
    item_cls = Button
    vantage_types = ["Button"]
    event_types = ["BTN"]
