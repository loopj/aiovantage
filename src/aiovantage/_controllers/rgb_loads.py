from aiovantage._controllers.query import QuerySet
from aiovantage.objects import VantageDDGColorLoad, VantageDGColorLoad

from .base import BaseController

RGBLoadTypes = VantageDDGColorLoad | VantageDGColorLoad
"""Types managed by the RGB loads controller."""


class RGBLoadsController(BaseController[RGBLoadTypes]):
    """RGB loads controller."""

    vantage_types = ("Vantage.DGColorLoad", "Vantage.DDGColorLoad")

    @property
    def on(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned off."""
        return self.filter(lambda load: not load.is_on)
