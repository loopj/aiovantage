from aiovantage.controllers import BaseController, QuerySet
from aiovantage.objects import Load, LoadGroup


class LoadGroupsController(BaseController[LoadGroup]):
    """Load groups controller."""

    vantage_types = ("LoadGroup",)

    def loads(self, vid: int) -> QuerySet[Load]:
        """Return a queryset of all loads in this load group."""
        load_group = self[vid]

        return self._vantage.loads.filter(lambda load: load.id in load_group.load_table)
