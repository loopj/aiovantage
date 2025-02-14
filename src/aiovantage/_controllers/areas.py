from aiovantage.objects import Area

from .base import Controller


class AreasController(Controller[Area]):
    """Areas controller."""

    vantage_types = ("Area",)
