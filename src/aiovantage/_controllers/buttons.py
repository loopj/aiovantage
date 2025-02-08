from aiovantage.objects import Button

from .base import BaseController


class ButtonsController(BaseController[Button]):
    """Buttons controller."""

    vantage_types = ("Button",)
