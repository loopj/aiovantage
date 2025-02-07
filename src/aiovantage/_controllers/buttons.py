from aiovantage.controllers import BaseController
from aiovantage.objects import Button


class ButtonsController(BaseController[Button]):
    """Buttons controller."""

    vantage_types = ("Button",)
