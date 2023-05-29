from typing import Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Load
from aiovantage.query import QuerySet

from .base import StatefulController
from .interfaces.load import LoadInterface


class LoadsController(StatefulController[Load], LoadInterface):
    # Store objects managed by this controller as Load instances
    item_cls = Load

    # Fetch Load objects from Vantage
    vantage_types = (Load,)

    # Get status updates from "STATUS LOAD"
    status_types = ("LOAD",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Load.

        self.update_state(id, {"level": await self.get_level(id)})

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle a state changes for a Load.

        if status == "LOAD":
            # STATUS LOAD
            # -> S:LOAD <id> <level (0-100)>
            level = float(args[0])
            self.update_state(id, {"level": level})

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""

        return self.filter(lambda load: load.level)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""

        return self.filter(lambda load: not load.level)

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
