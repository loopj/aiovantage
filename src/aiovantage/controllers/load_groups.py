"""Controller holding and managing Vantage load groups."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import Load, LoadGroup
from aiovantage.query import QuerySet

from .base import BaseController


class LoadGroupsController(BaseController[LoadGroup]):
    """Controller holding and managing Vantage load groups."""

    vantage_types = ("LoadGroup",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("LOAD",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, obj: LoadGroup) -> None:
        """Fetch the state properties of a load."""
        state = {
            "level": await obj.get_level(),
        }

        self.update_state(obj.vid, state)

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

    def loads(self, vid: int) -> QuerySet[Load]:
        """Return a queryset of all loads in this load group."""
        load_group = self[vid]

        return self._vantage.loads.filter(lambda load: load.id in load_group.load_table)
