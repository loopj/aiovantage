"""Controller holding and managing Vantage areas."""

from aiovantage.config_client.models import Area
from aiovantage.controllers.base import BaseController


class AreasController(BaseController[Area]):
    """Controller holding and managing Vantage areas."""

    vantage_types = ("Area",)
    """The Vantage object types that this controller will fetch."""
