"""Controller holding and managing Vantage areas."""

from aiovantage.models import Area

from .base import BaseController


class AreasController(BaseController[Area]):
    """Controller holding and managing Vantage areas."""

    vantage_types = ("Area",)
    """The Vantage object types that this controller will fetch."""
