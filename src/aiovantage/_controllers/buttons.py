from aiovantage.objects import Button

from .base import Controller


class ButtonsController(Controller[Button]):
    """Buttons controller."""

    vantage_types = ("Button",)
