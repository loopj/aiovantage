"""Controller holding and managing Vantage loads."""

from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import LoadInterface
from aiovantage.config_client.objects import Load
from aiovantage.query import QuerySet

from .base import StatefulController


class LoadsController(StatefulController[Load], LoadInterface):
    """Controller holding and managing Vantage loads."""

    # Fetch the following object types from Vantage
    vantage_types = ("Load",)

    # Get status updates from "STATUS LOAD"
    status_types = ("LOAD",)

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of a load."""

        state: Dict[str, Any] = {}
        state["level"] = await LoadInterface.get_level(self, vid)

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a load."""

        state: Dict[str, Any] = {}
        if status == "LOAD":
            state["level"] = LoadInterface.parse_load_status(args)

        self.update_state(vid, state)

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
