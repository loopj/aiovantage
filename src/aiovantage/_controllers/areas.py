from aiovantage.controllers import BaseController
from aiovantage.objects import Area


class AreasController(BaseController[Area]):
    """Areas controller."""

    vantage_types = ("Area",)
