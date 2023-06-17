"""Controller holding and managing Vantage load groups."""

from aiovantage.command_client.interfaces.load import LoadInterface
from aiovantage.config_client.objects import Load, LoadGroup
from aiovantage.query import QuerySet

from .base import BaseController


class LoadGroupsController(BaseController[LoadGroup], LoadInterface):
    """Controller holding and managing Vantage load groups."""

    # Fetch the following object types from Vantage
    vantage_types = ("LoadGroup",)

    def loads(self, vid: int) -> QuerySet[Load]:
        """Return a queryset of all loads in this load group."""

        load_group = self[vid]

        return self._vantage.loads.filter(lambda load: load.id in load_group.load_ids)
