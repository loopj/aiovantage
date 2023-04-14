import asyncio
import shlex
from typing import Sequence

from aiovantage.aci_client.system_objects import Load
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController
from aiovantage.vantage.query import QuerySet

# LOAD <load vid> <level (0-100)>
#   -> R:LOAD <load vid> <level (0-100)>

# RAMPLOAD <load vid> <level (0-100)> <seconds>
#   -> R:RAMPLOAD <load vid> <level (0-100)> <seconds>

# GETLOAD <load vid>
#   -> R:GETLOAD <load vid> <level (0-100)>

# STATUS LOAD
#   -> R:STATUS LOAD
#   -> S:LOAD <load vid> <level (0-100)>

# ADDSTATUS <load vid>
#   -> R:ADDSTATUS <load vid>
#   -> S:STATUS <load vid> Load.GetLevel <level (0-100000)>


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ("Load",)
    status_types = (StatusType.LOAD,)

    def _update_object_state(self, vid: int, args: Sequence[str]) -> None:
        # Update the state of a single Load.
        level = float(args[0])
        if vid in self:
            self[vid].level = level

    async def _fetch_object_state(self, vid: int) -> None:
        # Fetch initial state of a single Load.
        response = await self._vantage._hc_client.send_command(f"GETLOAD {vid}")
        _, _, *args = shlex.split(response)

        self._update_object_state(vid, args)

    async def _fetch_initial_states(self) -> None:
        # Fetch initial state of all Loads.
        await asyncio.gather(*[self._fetch_object_state(load.id) for load in self])

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

    async def set_level(self, vid: int, level: float) -> None:
        """Set the level of a load."""

        # Normalize level
        level = max(min(level, 100), 0)

        # Send command to controller
        await self._vantage._hc_client.send_command("LOAD", f"{vid}", f"{level}")

        # Update local level
        if vid in self:
            self[vid].level = level
