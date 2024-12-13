"""Controller holding and managing Vantage tasks."""

from typing_extensions import override

from aiovantage.controllers.base import BaseController
from aiovantage.models import Task
from aiovantage.object_interfaces import TaskInterface


class TasksController(BaseController[Task]):
    """Controller holding and managing Vantage tasks."""

    vantage_types = ("Task",)
    status_types = ("TASK",)
    interface_status_types = ("Task.IsRunning",)

    @override
    async def fetch_object_state(self, obj: Task) -> None:
        """Fetch the state properties of a task."""
        state = {
            "running": await TaskInterface.is_running(obj),
            "state": await TaskInterface.get_state(obj),
        }

        self.update_state(obj.id, state)

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
