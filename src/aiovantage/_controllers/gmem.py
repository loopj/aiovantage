from aiovantage.objects import GMem

from .base import Controller


class GMemController(Controller[GMem]):
    """GMem (variables) controller."""

    vantage_types = ("GMem",)
    force_category_status = True
