"""Controller holding and managing Vantage controllers."""

from contextlib import suppress
from typing import Any

from typing_extensions import override

from aiovantage.errors import CommandError
from aiovantage.objects import Master
from aiovantage.object_interfaces import (
    IntrospectionInterface,
    ObjectInterface,
)

from .base import BaseController


class MastersController(
    BaseController[Master], IntrospectionInterface, ObjectInterface
):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
    """The Vantage object types that this controller will fetch."""

    interface_status_types = ("Object.GetMTime",)
    """Which object interface status messages this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a Vantage controller."""
        state: dict[str, Any] = {
            "firmware_version": await self.get_version(),
        }

        # ObjectInterface is not available on 2.x firmware.
        with suppress(CommandError):
            state["last_updated"] = await ObjectInterface.get_mtime(self, vid)

        self.update_state(vid, state)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != "Object.GetMTime":
            return

        state = {
            "last_updated": self.parse_response(method, result, *args),
        }

        self.update_state(vid, state)

    async def get_version(self) -> str:
        """Get the firmware version of a Vantage controller.

        Returns:
            The firmware version of the controller.
        """
        # VERSION
        # -> R:VERSION {version}
        response = await self.command_client.command("VERSION")
        return response.args[0]
