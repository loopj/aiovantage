from aiovantage.objects import VantageDDGColorLoad, VantageDGColorLoad

from .base import Controller
from .query import QuerySet

RGBLoadTypes = VantageDDGColorLoad | VantageDGColorLoad
"""Types managed by the RGB loads controller."""


class RGBLoadsController(Controller[RGBLoadTypes]):
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
