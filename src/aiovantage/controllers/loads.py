import asyncio
import shlex
from typing import Sequence

from aiovantage.aci_client.system_objects import Load
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType
from aiovantage.query import QuerySet


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ("Load",)
    status_types = (StatusType.LOAD,)

    async def _fetch_initial_states(self) -> None:
        """Fetch initial state of all Loads."""

        await asyncio.gather(*[self._fetch_state(load.id) for load in self])

    def _update_object(self, vid: int, args: Sequence[str]) -> None:
        level = float(args[0])
        if vid in self:
            self[vid].level = level

    async def _fetch_state(self, vid: int) -> None:
        """Fetch initial state of a single Load."""

        response = await self._vantage._hc_client.send_command(f"GETLOAD {vid}")
        _, _, *args = shlex.split(response)

        self._update_object(vid, args)

    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are on."""

        return self._queryset.filter(lambda load: load.level)

    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are off."""

        return self._queryset.filter(lambda load: not load.level)

    async def turn_on(self, id: int) -> None:
        """Turn on a load."""

        await self.set_level(id, 100)

    async def turn_off(self, id: int) -> None:
        """Turn off a load."""

        await self.set_level(id, 0)

    async def set_level(self, id: int, level: float) -> None:
        """Set the level of a load."""

        # Normalize level
        level = max(min(level, 100), 0)

        # Send command to controller
        await self._vantage._hc_client.send_command("LOAD", f"{id}", f"{level}")

        # Update local level
        if id in self:
            self[id].level = level