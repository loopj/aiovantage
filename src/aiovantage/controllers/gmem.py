"""Controller holding and managing Vantage variables."""

from aiovantage.objects import GMem

from .base import BaseController


class GMemController(BaseController[GMem]):
    """Controller holding and managing Vantage variables."""

    vantage_types = ("GMem",)
    force_category_status = True
