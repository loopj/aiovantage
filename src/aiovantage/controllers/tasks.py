"""Controller holding and managing Vantage tasks."""

from typing import Sequence

from typing_extensions import override

from aiovantage.command_client.object_interfaces import TaskInterface
from aiovantage.models import Task

from .base import BaseController, State


class TasksController(BaseController[Task], TaskInterface):
    """Controller holding and managing Vantage tasks."""

    vantage_types = ("Task",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("TASK",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    object_status = True
    """Should this controller subscribe to "object status" events."""

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of a task."""
        return {
            "is_running": await TaskInterface.is_running(self, vid),
            "state": await TaskInterface.get_state(self, vid),
        }

    @override
    def parse_object_update(self, _vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for a task."""
        if status == "TASK":
            # STATUS TASK
            # -> S:TASK <id> <state>
            return {
                "state": int(args[0]),
            }

        if status == "Task.IsRunning":
            return {
                "is_running": TaskInterface.parse_is_running_status(args),
            }

        return None
