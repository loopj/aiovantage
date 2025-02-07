from aiovantage.controllers import BaseController
from aiovantage.objects import Master


class MastersController(BaseController[Master]):
    """Masters (InFusion Controllers) controller."""

    vantage_types = ("Master",)
