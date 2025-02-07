from aiovantage.objects import GMem

from .base import BaseController


class GMemController(BaseController[GMem]):
    """GMem (variables) controller."""

    vantage_types = ("GMem",)
    category_status = True
