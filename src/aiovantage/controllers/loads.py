import asyncio
import shlex
from typing import Sequence

from typing_extensions import override

from aiovantage.aci_client.system_objects import Load
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType
from aiovantage.query import QuerySet


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ("Load",)
    status_types = (StatusType.LOAD,)

    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are on."""

        return self._queryset.filter(lambda load: load.level)

    async def fetch_state(self) -> None:
        """Fetch initial state of all loads."""

        await asyncio.gather(*(self.get_level(load.id) for load in self))

    @override
    def status_handler(self, type: StatusType, id: int, args: Sequence[str]) -> None:
        # S:LOAD {vid} {level}
        level = float(args[0])

        # Update local level
        if id in self:
            self[id].level = level

    async def get_level(self, id: int) -> float:
        """Get the level of a load from the controller."""

        # Send command to controller
        response = await self._vantage._hc_client.send_command(f"GETLOAD {id}")

        # Parse response
        status_type, vid, *args = shlex.split(response)
        level = float(args[0])

        # Update local level
        if id in self:
            self[id].level = level

        return level

    async def set_level(self, id: int, level: float) -> None:
        """Set the level of a load."""

        # Normalize level
        level = max(min(level, 100), 0)

        # Send command to controller
        await self._vantage._hc_client.send_command("LOAD", f"{id}", f"{level}")

        # Update local level
        if id in self:
            self[id].level = level