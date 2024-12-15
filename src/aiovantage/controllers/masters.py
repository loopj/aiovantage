"""Controller holding and managing Vantage controllers."""

from typing import Any

from typing_extensions import override

from aiovantage.controllers.base import BaseController
from aiovantage.object_interfaces.object import ObjectInterface
from aiovantage.objects import Master


class MastersController(BaseController[Master]):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
    interface_status_types = ("Object.GetMTime",)

    @override
    async def fetch_object_state(self, obj: Master) -> None:
        """Fetch the state properties of a Vantage controller."""
        state: dict[str, Any] = {
            "firmware_version": await self.get_version(),
        }

        self.update_state(obj.id, state)

    @override
    def handle_object_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != "Object.GetMTime":
            return

        state = {
            "mtime": ObjectInterface.parse_response(method, result, *args),
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
