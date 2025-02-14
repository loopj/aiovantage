from aiovantage.objects import Load, LoadGroup

from .base import Controller
from .query import QuerySet


class LoadsController(Controller[Load]):
    """Loads controller."""

    vantage_types = ("Load",)

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""
        return self.filter(lambda load: not load.is_on)

    @property
    def relays(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are relays."""
        return self.filter(lambda load: load.is_relay)

    @property
    def motors(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are motors."""
        return self.filter(lambda load: load.is_motor)

    @property
    def lights(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are lights."""
        return self.filter(lambda load: load.is_light)

    def in_load_group(self, load_group: LoadGroup) -> QuerySet[Load]:
        """Return a queryset of all loads in the given load group."""
        return self.filter(lambda load: load.vid in load_group.load_table)
