from aiovantage.objects import Master

from .base import BaseController


class MastersController(BaseController[Master]):
    """Masters (InFusion Controllers) controller."""

    vantage_types = ("Master",)
