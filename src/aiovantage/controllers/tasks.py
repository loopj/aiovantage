from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import TaskInterface
from aiovantage.config_client.objects import Task

from .base import StatefulController


class TasksController(StatefulController[Task], TaskInterface):
    # Fetch the following object types from Vantage
    vantage_types = ("Task",)

    # Subscribe to status updates from the event log for the following methods
    event_log_status = True
    event_log_status_methods = ("Task.IsRunning", "Task.GetState")

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Task.

        state: Dict[str, Any] = {}
        state["is_running"] = await TaskInterface.is_running(self, id)
        state["state"] = await TaskInterface.get_state(self, id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, method: str, args: Sequence[str]) -> None:
        # Handle state changes for a Task.

        state: Dict[str, Any] = {}
        if method == "Task.IsRunning":
            state["is_running"] = TaskInterface.parse_is_running_status(args)

        elif method == "Task.GetState":
            state["state"] = TaskInterface.parse_get_state_status(args)

        self.update_state(id, state)
