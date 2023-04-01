import asyncio

from aiovantage.query import QuerySet

from ..clients.hc import StatusType
from ..models.load import Load
from .base import BaseController


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ("Load",)
    status_types = (StatusType.LOAD,)

    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are on."""
        return self._queryset.filter(lambda load: load._level)

    async def fetch_state(self) -> None:
        """Fetch initial state of all loads."""
        await asyncio.gather(*(load.get_level() for load in self))
