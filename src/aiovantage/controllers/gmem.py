"""Controller holding and managing Vantage variables."""

from typing import Any, Dict, Sequence, Union

from typing_extensions import override

from aiovantage.command_client.interfaces import GMemInterface
from aiovantage.config_client.objects import GMem
from aiovantage.controllers.base import BaseController


class GMemController(BaseController[GMem], GMemInterface):
    """Controller holding and managing Vantage variables."""

    # Fetch the following object types from Vantage
    vantage_types = ("GMem",)

    # Get status updates from "STATUS VARIABLE"
    status_types = ("VARIABLE",)

    @override
    async def fetch_object_state(self, vid: int) -> Dict[str, Any]:
        """Fetch the state properties of a variable."""

        return {
            "value": self._parse_value(vid, await self.get_value(vid)),
        }

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for a variable."""

        state: Dict[str, Any] = {}
        if status == "VARIABLE":
            raw_value = GMemInterface.parse_variable_status(args)
            state["value"] = self._parse_value(vid, raw_value)

        self.update_state(vid, state)

    def _parse_value(self, vid: int, value: str) -> Union[int, str, bool]:
        # Parse the results of a GMem lookup into the expected type.

        gmem: GMem = self[vid]

        if gmem.is_bool:
            return bool(int(value))
        if gmem.is_str:
            return value

        return int(value)
