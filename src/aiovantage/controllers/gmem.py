"""Controller holding and managing Vantage variables."""

import re

from typing_extensions import override

from aiovantage.command_client.utils import parse_byte_param
from aiovantage.objects import GMem

from .base import BaseController


class GMemController(BaseController[GMem]):
    """Controller holding and managing Vantage variables.

    We use the `GETVARIABLE` and `VARIABLE` wrappers for getting and setting
    variable values, rather than the GMem object interface, since they are much
    simpler than working with raw byte arrays.
    """

    vantage_types = ("GMem",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("VARIABLE",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a variable."""
        state = {
            "value": await self.get_value(vid),
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "VARIABLE":
            return

        # STATUS VARIABLE
        # -> S:VARIABLE <id> <value>
        state = {
            "value": self._parse_value(vid, args[0]),
        }

        self.update_state(vid, state)

    async def get_value(self, vid: int) -> int | str | bool:
        """Get the value of a variable.

        Args:
            vid: The Vantage ID of the variable.

        Returns:
            The value of the variable, either a bool, int, or str.
        """
        # GETVARIABLE {id}
        # -> R:GETVARIABLE {id} {value}
        response = await self.command_client.command("GETVARIABLE", vid)
        raw_value = response.args[1]

        return self._parse_value(vid, raw_value)

    async def set_value(self, vid: int, value: int | str | bool) -> None:
        """Set the value of a variable.

        Args:
            vid: The Vantage ID of the variable.
            value: The value to set, either a bool, int, or str.
        """
        # VARIABLE {id} {value}
        # -> R:VARIABLE {id} {value}
        await self.command_client.command("VARIABLE", vid, value, force_quotes=True)

    def _parse_value(self, vid: int, value: str) -> int | str | bool:
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
