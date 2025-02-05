"""Areas controller."""

from aiovantage.objects import Area

from .base import BaseController


class AreasController(BaseController[Area]):
    """Areas controller."""

    vantage_types = ("Area",)
