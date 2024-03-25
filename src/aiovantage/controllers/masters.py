"""Controller holding and managing Vantage controllers."""

from contextlib import suppress
from typing import Any

from typing_extensions import override

from aiovantage.command_client.object_interfaces import (
    IntrospectionInterface,
    ObjectInterface,
)
from aiovantage.errors import CommandError
from aiovantage.models import Master

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
        state: dict[str, Any] = {}

        # IntrospectionInterface is not available on 2.x firmware.
        with suppress(CommandError):
            state["firmware_version"] = (
                await IntrospectionInterface.get_firmware_version(
                    self, vid, self.Firmware.Application
                )
            )

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
