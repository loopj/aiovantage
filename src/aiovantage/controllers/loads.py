"""Controller holding and managing Vantage loads."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import Load
from aiovantage.query import QuerySet

from .base import BaseController


class LoadsController(BaseController[Load]):
    """Controller holding and managing Vantage loads."""

    vantage_types = ("Load",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("LOAD",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    def handle_status(self, obj: Load, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "LOAD":
            return

        # STATUS LOAD
        # -> S:LOAD <id> <level (0-100)>
        state = {
            "level": Decimal(args[0]),
        }

        self.update_state(obj, state)

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
