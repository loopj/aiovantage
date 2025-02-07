from aiovantage.controllers import BaseController
from aiovantage.objects import GMem


class GMemController(BaseController[GMem]):
    """GMem (variables) controller."""

    vantage_types = ("GMem",)
    category_status = True
