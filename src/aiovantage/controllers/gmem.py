"""Controller holding and managing Vantage variables."""
import re
from typing import Sequence, Union

from typing_extensions import override

from aiovantage.command_client.interfaces import GMemInterface
from aiovantage.command_client.utils import parse_byte_param
from aiovantage.config_client.objects import GMem
from aiovantage.controllers.base import BaseController, State


class GMemController(BaseController[GMem], GMemInterface):
    """Controller holding and managing Vantage variables."""

    vantage_types = ("GMem",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("VARIABLE",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a variable."""
        return {
            "value": self._parse_value(vid, await self.get_value(vid)),
        }

    @override
    def parse_object_update(self, vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a variable."""
        if status != "VARIABLE":
            return None

        return {
            "value": self._parse_value(vid, GMemInterface.parse_variable_status(args)),
        }

    def _parse_value(self, vid: int, value: str) -> Union[int, str, bool]:
        # Parse the results of a GMem lookup into the expected type.
        gmem: GMem = self[vid]

        if gmem.is_bool:
            return bool(int(value))
        if gmem.is_str:
            # Handle byte array strings
            if re.match(r"^[\[\{].*[\]\}]$", value):
                byte_param = parse_byte_param(value)
                return byte_param.decode().rstrip("\x00")

            return value

        return int(value)
