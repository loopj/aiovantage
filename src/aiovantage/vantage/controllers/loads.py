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
    vantage_types = (Load,)
    status_types = (StatusType.LOAD,)

    def _update_object_state(self, vid: int, args: Sequence[str]) -> None:
        if vid not in self:
            return

        # Update the state of a single Load.
        self[vid].level = float(args[0])

    async def _fetch_object_state(self, vid: int) -> None:
        # Fetch initial state of a single Load.
        response = await self._vantage._hc_client.send_command("GETLOAD", f"{vid}")

        # GETLOAD <load vid> <level (0-100)>
        _, _, *args = shlex.split(response)

        self._update_object_state(vid, args)

    async def _fetch_initial_states(self) -> None:
        # Fetch initial state of all Loads.
        await asyncio.gather(*[self._fetch_object_state(load.id) for load in self])

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""

        return self.filter(lambda load: load.level)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""

        return self.filter(lambda load: not load.level)

    async def turn_on(self, id: int) -> None:
        """
        Turn on a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 100)

    async def turn_off(self, id: int) -> None:
        """
        Turn off a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 0)

    async def set_level(self, vid: int, level: float) -> None:
        """
        Set the level of a load.

        Args:
            vid: The ID of the load.
            level: The level to set the load to (0-100).
        """

        if vid not in self:
            return

        # Normalize level
        level = max(min(level, 100), 0)

        # Send command to controller
        await self._vantage._hc_client.send_command("LOAD", f"{vid}", f"{level}")

        # Update local level
        self[vid].level = level
