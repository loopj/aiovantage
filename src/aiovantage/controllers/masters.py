"""Controller holding and managing Vantage controllers."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import IntrospectionInterface, ObjectInterface
from aiovantage.config_client.objects import Master
from aiovantage.controllers.base import BaseController, State


class MastersController(
    BaseController[Master],
    ObjectInterface,
    IntrospectionInterface,
):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
    """The Vantage object types that this controller will fetch."""

    enhanced_log_status_methods = ("Object.GetMTime",)
    """Which status methods this controller handles from the Enhanced Log."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a Vantage controller."""
        return {
            "last_updated": await ObjectInterface.get_mtime(self, vid),
            "firmware_version": await IntrospectionInterface.get_firmware_version(
                self, vid, IntrospectionInterface.Firmware.APPLICATION
            ),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a Vantage controller."""
        if status != "Object.GetMTime":
            return None

        return {
            "last_updated": ObjectInterface.parse_get_mtime_status(args),
        }
