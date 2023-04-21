from typing import Any, Dict, Optional, Sequence

from aiovantage.aci_client.system_objects import Load
from aiovantage.vantage.controllers.base import BaseController
from aiovantage.vantage.query import QuerySet


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = (Load,)
    status_types = ("LOAD",)

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""

        return self.filter(lambda load: load.level)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""

        return self.filter(lambda load: not load.level)

    async def turn_on(self, id: int, transition: Optional[float] = None) -> None:
        """Turn on a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 100, transition)

    async def turn_off(self, id: int, transition: Optional[float] = None) -> None:
        """Turn off a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 0, transition)

    async def get_level(self, id: int) -> float:
        """Get the level of a load.

        Args:
            id: The ID of the load.
        """

        # GETLOAD <load vid>
        # -> R:GETLOAD <load vid> <level (0-100)>
        response = await self._hc_client.command("GETLOAD", id)
        level = float(response[1])

        return level

    async def set_level(
        self, id: int, level: float, transition: Optional[float] = None
    ) -> None:
        """Set the level of a load.

        Args:
            id: The ID of the load.
            level: The level to set the load to (0-100).
        """

        # Clamp level to 0-100
        level = max(min(level, 100), 0)

        # Don't send a command if the level isn't changing
        if self[id].level == level:
            return

        # LOAD <id> <level>
        # -> R:LOAD <id> <level>
        if transition is not None:
            await self._hc_client.command("RAMPLOAD", id, level, transition)
        else:
            await self._hc_client.command("LOAD", id, level)

        # Update local state
        self._update_and_notify(id, level=level)

    async def _fetch_initial_state(self, id: int) -> None:
        # Fetch initial state of all Loads.

        self._update_and_notify(id, level=await self.get_level(id))

    def _handle_status(self, id: int, status_type: str, args: Sequence[str]) -> None:
        # Handle a status update for a Load.

        state: Dict[str, Any] = {}

        if status_type == "LOAD":
            # S:LOAD <id> <level (0-100)>
            state["level"] = float(args[0])

        self._update_and_notify(id, **state)
