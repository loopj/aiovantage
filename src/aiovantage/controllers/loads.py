"""Controller holding and managing Vantage loads."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import Load
from aiovantage.query import QuerySet

from .base import BaseController


class LoadsController(BaseController[Load]):
    """Controller holding and managing Vantage loads."""

    vantage_types = (Load,)
    status_types = ("LOAD",)

    @override
    async def fetch_object_state(self, obj: Load) -> None:
        """Fetch the state properties of a load."""
        state = {
            "level": await obj.get_level(),
        }

        self.update_state(obj.id, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "LOAD":
            return

        # STATUS LOAD
        # -> S:LOAD <id> <level (0-100)>
        state = {
            "level": Decimal(args[0]),
        }

        self.update_state(vid, state)

    @property
    def is_on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def is_off(self) -> QuerySet[Load]:
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
