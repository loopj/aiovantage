"""Controller holding and managing Vantage loads."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import LoadInterface
from aiovantage.config_client.objects import Load
from aiovantage.query import QuerySet

from .base import BaseController, State


class LoadsController(BaseController[Load], LoadInterface):
    """Controller holding and managing Vantage loads."""

    # Fetch the following object types from Vantage
    vantage_types = ("Load",)

    # Get status updates from "STATUS LOAD"
    status_types = ("LOAD",)

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a load."""
        return {
            "level": await LoadInterface.get_level(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a load."""
        if status != "LOAD":
            return None

        return {
            "level": LoadInterface.parse_load_status(args),
        }

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
