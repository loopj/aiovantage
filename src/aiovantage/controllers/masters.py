"""Controller holding and managing Vantage controllers."""

from typing_extensions import override

from aiovantage.objects import Master

from .base import BaseController


class MastersController(BaseController[Master]):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
    """The Vantage object types that this controller will fetch."""

    interface_status_types = ("Object.GetMTime",)
    """Which object interface status messages this controller handles, if any."""

    @override
    def handle_interface_status(
        self, obj: Master, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != "Object.GetMTime":
            return

        state = {
            "m_time": obj.parse_object_status(method, result, *args),
        }

        self.update_state(obj, state)
