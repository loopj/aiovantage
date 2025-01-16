"""Controller holding and managing Vantage loads."""

from aiovantage.objects import Load, LoadGroup
from aiovantage.query import QuerySet

from .base import BaseController

LoadTypes = Load | LoadGroup


class LoadsController(BaseController[LoadTypes]):
    """Controller holding and managing Vantage loads."""

    vantage_types = (Load, LoadGroup)

    @property
    def on(self) -> QuerySet[LoadTypes]:
        """Return a queryset of all loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[LoadTypes]:
        """Return a queryset of all loads that are turned off."""
        return self.filter(lambda load: not load.is_on)
