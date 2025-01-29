"""Controller holding and managing Vantage areas."""

from aiovantage.objects import Area

from .base import BaseController


class AreasController(BaseController[Area]):
    """Controller holding and managing Vantage areas."""

    vantage_types = ("Area",)
