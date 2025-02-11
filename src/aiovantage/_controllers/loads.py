from aiovantage._controllers.query import QuerySet
from aiovantage.objects import Load, LoadGroup

from .base import BaseController

LoadTypes = Load | LoadGroup
"""Types managed by the loads controller."""


class LoadsController(BaseController[LoadTypes]):
    """Loads controller."""

    vantage_types = ("Load", "LoadGroup")

    @property
    def on(self) -> QuerySet[LoadTypes]:
        """Return a queryset of all loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[LoadTypes]:
        """Return a queryset of all loads that are turned off."""
        return self.filter(lambda load: not load.is_on)
