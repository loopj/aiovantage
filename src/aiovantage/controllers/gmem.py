from typing import Any, Dict, Sequence, Union

from typing_extensions import override

from aiovantage.command_client.interfaces import GMemInterface
from aiovantage.config_client.objects import GMem
from aiovantage.controllers.base import StatefulController


class GMemController(StatefulController[GMem], GMemInterface):
    # Fetch the following object types from Vantage
    vantage_types = ("GMem",)

    # Get status updates from "STATUS VARIABLE"
    status_types = ("VARIABLE",)

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of all GMem objects.

        state: Dict[str, Any] = {}

        raw_value = await self.get_value(id)
        state["value"] = self._parse_value(id, raw_value)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a GMem object.

        state: Dict[str, Any] = {}
        if status == "VARIABLE":
            raw_value = GMemInterface.parse_variable_status(args)
            state["value"] = self._parse_value(id, raw_value)

        self.update_state(id, state)

    def _parse_value(self, id: int, value: str) -> Union[int, str, bool]:
        # Parse the results of a GMem lookup into the expected type.

        gmem: GMem = self[id]
        if gmem.is_bool:
            return bool(int(value))
        elif gmem.is_str:
            return value
        else:
            return int(value)
