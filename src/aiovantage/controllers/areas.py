"""Controller holding and managing Vantage areas."""

from aiovantage.controllers.base import BaseController
from aiovantage.models import Area


class AreasController(BaseController[Area]):
    """Controller holding and managing Vantage areas."""

    vantage_types = ("Area",)
