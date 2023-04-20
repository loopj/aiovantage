from typing import Sequence

from aiovantage.aci_client.system_objects import Load
from aiovantage.hc_client import StatusCategory
from aiovantage.vantage.controllers.base import BaseController
from aiovantage.vantage.query import QuerySet


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = (Load,)
    status_categories = (StatusCategory.LOAD,)

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""

        return self.filter(lambda load: load.level)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""

        return self.filter(lambda load: not load.level)

    async def turn_on(self, id: int) -> None:
        """Turn on a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 100)

    async def turn_off(self, id: int) -> None:
        """Turn off a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 0)

    async def get_level(self, id: int) -> float:
        """Get the level of a load.

        Args:
            id: The ID of the load.
        """

        # GETLOAD <load vid>
        # -> R:GETLOAD <load vid> <level (0-100)>
        response = await self.command_client.send_command("GETLOAD", id)
        level = float(response[1])

        return level

    async def set_level(self, id: int, level: float) -> None:
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
        await self.command_client.send_command("LOAD", id, level)

        # Update local state
        self._update_state(id, level=level)

    async def _fetch_initial_state(self) -> None:
        # Fetch initial state of all Loads.

        for obj in self:
            obj.level = await self.get_level(obj.id)

    def _handle_category_status(
        self, category: StatusCategory, id: int, args: Sequence[str]
    ) -> None:
        # Handle "STATUS" category status messages

        # S:LOAD <id> <level (0-100)>
        self._update_state(id, level=float(args[0]))