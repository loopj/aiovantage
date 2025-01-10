"""Controller holding and managing Vantage controllers."""

from typing_extensions import override

from aiovantage.object_interfaces import ObjectInterface
from aiovantage.objects import Master

from .base import BaseController


class MastersController(BaseController[Master]):
    """Controller holding and managing Vantage controllers."""

    vantage_types = (Master,)
    interface_status_types = ("Object.GetMTime",)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != "Object.GetMTime":
            return

        state = {
            "m_time": ObjectInterface.parse_status(method, result, *args),
        }

        self.update_state(vid, state)
