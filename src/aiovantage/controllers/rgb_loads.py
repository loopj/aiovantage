"""Controller holding and managing Vantage RGB loads."""

from aiovantage.objects import VantageDDGColorLoad, VantageDGColorLoad
from aiovantage.query import QuerySet

from .base import BaseController

RGBLoadTypes = VantageDGColorLoad | VantageDDGColorLoad


class RGBLoadsController(BaseController[RGBLoadTypes]):
    """Controller holding and managing Vantage RGB loads."""

    vantage_types = (VantageDGColorLoad, VantageDDGColorLoad)

    @property
    def on(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned off."""
        return self.filter(lambda load: not load.is_on)
