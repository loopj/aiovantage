"""Controller holding and managing Vantage tasks."""

from typing_extensions import override

from aiovantage.object_interfaces import TaskInterface
from aiovantage.objects import Task

from .base import BaseController


class TasksController(BaseController[Task]):
    """Controller holding and managing Vantage tasks."""

    vantage_types = (Task,)
    status_types = ("TASK",)
    interface_status_types = ("Task.IsRunning",)

    @override
    async def fetch_object_state(self, obj: Task) -> None:
        """Fetch the state properties of a task."""
        state = {
            "running": await obj.is_running(),
            "state": await obj.get_state(),
        }

        self.update_state(obj.vid, state)

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
            "running": TaskInterface.parse_response(method, result, *args),
        }

        self.update_state(vid, state)
