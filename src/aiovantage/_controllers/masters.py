from aiovantage.objects import Master

from .base import Controller


class MastersController(Controller[Master]):
    """Masters (InFusion Controllers) controller."""

    vantage_types = ("Master",)
