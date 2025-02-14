from aiovantage.objects import LoadGroup

from .base import Controller


class LoadGroupsController(Controller[LoadGroup]):
    """Load groups controller."""

    vantage_types = ("LoadGroup",)
