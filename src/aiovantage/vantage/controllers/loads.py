from typing import Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Load
from aiovantage.vantage.controllers.base import StatefulController
from aiovantage.vantage.query import QuerySet


class LoadsController(StatefulController[Load]):
    # Store objects managed by this controller as Load instances
    item_cls = Load

    # Fetch Load objects from Vantage
    vantage_types = (Load,)

    # Get status updates from "STATUS LOAD"
    status_types = ("LOAD",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Load.

        self.update_state(id, {"level": await self.get_level(id)})

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle a state changes for a Load.

        if status == "LOAD":
            # STATUS LOAD
            # -> S:LOAD <id> <level (0-100)>
            level = float(args[0])
            self.update_state(id, {"level": level})

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""

        return self.filter(lambda load: load.level)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""

        return self.filter(lambda load: not load.level)

    @property
    def relays(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are relays."""

        return self.filter(lambda load: load.is_relay)

    @property
    def motors(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are motors."""

        return self.filter(lambda load: load.is_motor)

    async def turn_on(self, id: int, transition: float = 0) -> None:
        """
        Turn on a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 100, transition)

    async def turn_off(self, id: int, transition: float = 0) -> None:
        """
        Turn off a load.

        Args:
            id: The ID of the load.
        """

        await self.set_level(id, 0, transition)

    async def get_level(self, id: int) -> float:
        """
        Get the level of a load.

        Args:
            id: The ID of the load.
        """

        # GETLOAD <load vid>
        # -> R:GETLOAD <load vid> <level (0-100)>
        response = await self.command_client.command("GETLOAD", id)
        level = float(response.args[1])

        return level

    async def set_level(self, id: int, level: float, transition: float = 0) -> None:
        """
        Set the level of a load.

        Args:
            id: The ID of the load.
            level: The level to set the load to (0-100).
        """

        # Clamp level to 0-100
        level = max(min(level, 100), 0)

        # Don't send a command if the level isn't changing
        if id in self and self[id].level == level:
            return

        if transition:
            # RAMPLOAD <id> <level> <seconds>
            # -> R:RAMPLOAD <id> <level> <seconds>
            await self.command_client.command("RAMPLOAD", id, level, transition)
        else:
            # LOAD <id> <level>
            # -> R:LOAD <id> <level>
            await self.command_client.command("LOAD", id, level)

        # Update local state
        self.update_state(id, {"level": level})
