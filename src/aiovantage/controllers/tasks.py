from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.command_client.interfaces import TaskInterface
from aiovantage.config_client.objects import Task

from .base import StatefulController


class TasksController(StatefulController[Task], TaskInterface):
    # Store objects managed by this controller as Task instances
    item_cls = Task

    # Fetch Task objects from Vantage
    vantage_types = (Task,)

    # Subscribe to status updates from the event log for the following methods
    event_log_status_methods = ("Task.IsRunning", "Task.GetState")

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Task.

        state: Dict[str, Any] = {}
        state["is_running"] = await self.is_running(id)
        state["state"] = await self.get_state(id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, method: str, args: Sequence[str]) -> None:
        # Handle state changes for a Task.

        state: Dict[str, Any] = {}
        if method == "Task.IsRunning":
            # <id> Task.IsRunning <0/1>
            state["is_running"] = bool(int(args[0]))

        elif method == "Task.GetState":
            # <id> Task.GetState <0/1>
            state["state"] = bool(int(args[0]))

        self.update_state(id, state)
