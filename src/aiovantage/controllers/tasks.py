from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Task
from aiovantage.controllers.base import StatefulController

# Event types:
#   PRESS, RELEASE, HOLD, TIMER, DATA, POSITION, INRANGE, OUTOFRANGE, TEMPERATURE,
#   DAYMODE, FANMODE, OPERATIONMODE, CONNECT, DISCONNECT, BOOT, LEARN, CANCEL, NONE


class TasksController(StatefulController[Task]):
    # Store objects managed by this controller as Task instances
    item_cls = Task

    # Fetch Task objects from Vantage
    vantage_types = (Task,)

    # Get status updates from the event log
    event_log_status = True

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of a Task.

        state: Dict[str, Any] = {}
        state["is_running"] = await self.is_running(id)
        state["state"] = await self.get_state(id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for a Task.

        state: Dict[str, Any] = {}
        if status == "Task.IsRunning":
            # <id> Task.IsRunning <0/1>

            state["is_running"] = bool(int(args[0]))

        elif status == "Task.GetState":
            # <id> Task.GetState <0/1>

            state["state"] = bool(int(args[0]))

        self.update_state(id, state)

    async def get_state(self, id: int) -> bool:
        """
        Get the state of a task.

        Args:
            id: The ID of the task.
        """

        # GETTASK <id>
        # -> R:GETTASK <id> <state 0/1>

        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state (0/1)> Task.GetState
        response = await self.command_client.command("INVOKE", id, "Task.GetState")
        task_state = bool(int(response.args[1]))

        return task_state

    async def is_running(self, id: int) -> bool:
        """
        Get the running state of a task.

        Args:
            id: The ID of the task.
        """

        # INVOKE <id> Task.IsRunning
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        response = await self.command_client.command("INVOKE", id, "Task.IsRunning")
        is_running = bool(int(response.args[1]))

        return is_running

    async def start(self, id: int, event: str = "RELEASE") -> None:
        """
        Start a task.

        Args:
            id: The ID of the task.
            event: The event to send to the task.
        """

        # TASK <id> <event>
        # -> R:TASK <task vid> <event>
        await self.command_client.command("TASK", id, event)
