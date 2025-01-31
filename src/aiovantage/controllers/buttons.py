"""Controller holding and managing Vantage buttons."""

from aiovantage.objects import Button

from .base import BaseController


class ButtonsController(BaseController[Button]):
    """Controller holding and managing Vantage buttons."""

    vantage_types = ("Button",)
