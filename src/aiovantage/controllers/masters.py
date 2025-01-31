"""Controller holding and managing Vantage controllers."""

from aiovantage.objects import Master

from .base import BaseController


class MastersController(BaseController[Master]):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
