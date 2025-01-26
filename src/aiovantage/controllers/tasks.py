"""Controller holding and managing Vantage tasks."""

from typing_extensions import override

from aiovantage.object_interfaces import TaskInterface
from aiovantage.objects import Task

from .base import BaseController


class TasksController(BaseController[Task], TaskInterface):
    """Controller holding and managing Vantage tasks."""

    vantage_types = ("Task",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("TASK",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    interface_status_types = ("Task.IsRunning",)
    """Which object interface status messages this controller handles, if any."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a task."""
        state = {
            "is_running": await TaskInterface.is_running(self, vid),
            "state": await TaskInterface.get_state(self, vid),
        }

        self.update_state(vid, state)

    @override
    def handle_status(self, vid: int, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "TASK":
            return

        # STATUS TASK
        # -> S:TASK <id> <state>
        state = {
            "state": int(args[0]),
        }

        self.update_state(vid, state)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        if method != "Task.IsRunning":
            return

        state = {
            "is_running": self.parse_object_status(method, result, *args),
        }

        self.update_state(vid, state)
