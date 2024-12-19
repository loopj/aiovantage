"""Controller holding and managing Vantage controllers."""

from contextlib import suppress
from typing import Any

from typing_extensions import override

from aiovantage.errors import CommandError
from aiovantage.object_interfaces import ObjectInterface
from aiovantage.objects import Master

from .base import BaseController


class MastersController(BaseController[Master]):
    """Controller holding and managing Vantage controllers."""

    vantage_types = (Master,)
    interface_status_types = ("Object.GetMTime",)

    @override
    async def fetch_object_state(self, obj: Master) -> None:
        """Fetch the state properties of a Vantage controller."""
        state: dict[str, Any] = {}

        # ObjectInterface is not available on 2.x firmware.
        with suppress(CommandError):
            state["m_time"] = await obj.get_mtime()

        self.update_state(obj.id, state)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != "Object.GetMTime":
            return

        state = {
            "m_time": ObjectInterface.parse_response(method, result, *args),
        }

        self.update_state(vid, state)
