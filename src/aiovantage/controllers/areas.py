"""Controller holding and managing Vantage areas."""

from aiovantage.config_client.objects import Area
from aiovantage.controllers.base import BaseController


class AreasController(BaseController[Area]):
    """Controller holding and managing Vantage areas."""

    # Fetch the following object types from Vantage
    vantage_types = ("Area",)
