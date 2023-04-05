import asyncio

from aiovantage.hc_client import StatusType
from aiovantage.controllers.base import BaseController
from aiovantage.models.load import Load
from aiovantage.query import QuerySet


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
