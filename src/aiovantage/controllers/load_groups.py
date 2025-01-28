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
    def handle_category_status(self, obj: LoadGroup, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "LOAD":
            return

        # STATUS LOAD
        # -> S:LOAD <id> <level (0-100)>
        state = {
            "level": Decimal(args[0]),
        }

        self.update_state(obj, state)

    def loads(self, vid: int) -> QuerySet[Load]:
        """Return a queryset of all loads in this load group."""
        load_group = self[vid]

        return self._vantage.loads.filter(lambda load: load.id in load_group.load_table)
