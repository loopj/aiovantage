"""Controller holding and managing Vantage RGB loads."""

from aiovantage.objects import VantageDDGColorLoad, VantageDGColorLoad
from aiovantage.query import QuerySet

from .base import BaseController

# The various "rgb load" object types don't all inherit from the same base class,
# so for typing purposes we'll use a union of all the types.
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
