from aiovantage.objects import LoadGroup

from .base import BaseController


class LoadGroupsController(BaseController[LoadGroup]):
    """Load groups controller."""

    vantage_types = ("LoadGroup",)
