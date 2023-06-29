"""Controller holding and managing Vantage tasks."""

from typing import Any, Dict, Optional, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import TaskInterface
from aiovantage.config_client.objects import Task

from .base import BaseController


class TasksController(BaseController[Task], TaskInterface):
    """Controller holding and managing Vantage tasks."""

    # Fetch the following object types from Vantage
    vantage_types = ("Task",)

    # Subscribe to status updates from the Enhanced Log for the following methods
    enhanced_log_status = True
    enhanced_log_status_methods = ("Task.IsRunning", "Task.GetState")

    @override
    async def fetch_object_state(self, vid: int) -> Optional[Dict[str, Any]]:
        """Fetch the state properties of a task."""

        return {
            "is_running": await TaskInterface.is_running(self, vid),
            "state": await TaskInterface.get_state(self, vid),
        }

    @override
    def parse_object_update(
        self, _vid: int, status: str, args: Sequence[str]
    ) -> Optional[Dict[str, Any]]:
        """Handle state changes for a task."""

        if status == "Task.IsRunning":
            return {
                "is_running": TaskInterface.parse_is_running_status(args),
            }

        if status == "Task.GetState":
            return {
                "state": TaskInterface.parse_get_state_status(args),
            }

        return None
