"""Controller holding and managing Vantage load groups."""

from aiovantage.objects import Load, LoadGroup
from aiovantage.query import QuerySet

from .base import BaseController


class LoadGroupsController(BaseController[LoadGroup]):
    """Controller holding and managing Vantage load groups."""

    vantage_types = ("LoadGroup",)
    status_categories = ("LOAD",)

    def loads(self, vid: int) -> QuerySet[Load]:
        """Return a queryset of all loads in this load group."""
        load_group = self[vid]

        return self._vantage.loads.filter(lambda load: load.id in load_group.load_table)
