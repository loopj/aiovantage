"""Controller holding and managing Vantage load groups."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces.load import LoadInterface
from aiovantage.config_client.models import Load, LoadGroup
from aiovantage.query import QuerySet

from .base import BaseController, State


class LoadGroupsController(BaseController[LoadGroup], LoadInterface):
    """Controller holding and managing Vantage load groups."""

    vantage_types = ("LoadGroup",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("LOAD",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

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

    def loads(self, vid: int) -> QuerySet[Load]:
        """Return a queryset of all loads in this load group."""
        load_group = self[vid]

        return self._vantage.loads.filter(lambda load: load.id in load_group.load_ids)
