from enum import Enum
from typing import Any, Dict, Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Task
from aiovantage.controllers.base import StatefulController


class EventType(Enum):
    CANCEL = (-2, "CANCEL")
    NONE = (-1, "NONE")
    RELEASE = (0, "RELEASE")
    PRESS = (1, "PRESS")
    HOLD = (2, "HOLD")
    TIMER = (3, "TIMER")
    DATA = (4, "DATA")
    POSITION = (5, "POSITION")
    INRANGE = (6, "INRANGE")
    OUTOFRANGE = (7, "OUTOFRANGE")
    TEMPERATURE = (8, "TEMPERATURE")
    DAYMODE = (9, "DAYMODE")
    FANMODE = (10, "FANMODE")
    OPERATIONMODE = (11, "OPERATIONMODE")
    CONNECT = (12, "CONNECT")
    DISCONNECT = (13, "DISCONNECT")
    BOOT = (14, "BOOT")
    LEARN = (15, "LEARN")

    @property
    def id(self) -> int:
        return self.value[0]

    @property
    def name(self) -> str:
        return self.value[1]


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

    async def get_state(self, id: int) -> bool:
        """
        Get the state of a task.

        Args:
            id: The ID of the task.
        """

        # GETTASK <id>
        # -> R:GETTASK <id> <state 0/1>
        # response = await self.command_client.command("GETTASK", id)
        # task_state = bool(int(response.args[1]))

        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state (0/1)> Task.GetState
        response = await self.command_client.command("INVOKE", id, "Task.GetState")
        task_state = bool(int(response.args[1]))

        return task_state

    async def start(
        self, id: int, *, event_type: EventType = EventType.RELEASE, source_id: int = 0
    ) -> None:
        """
        Start a task.

        Args:
            id: The ID of the task.
            event_type: The type event to send to the task, defaults to RELEASE.
            source_id: The object ID of the source sending the event, defaults to 0.
        """

        # TASK <id> <event>
        # -> R:TASK <task vid> <event>
        # await self.command_client.command("TASK", id, event_type.name)

        # INVOKE <id> Task.Start <source> <event> <param1> <param2>
        # -> R:INVOKE <id> <rcode (0/1)> Task.Start <source> <event> <param1> <param2>
        await self.command_client.command(
            "INVOKE", id, "Task.Start", source_id, event_type.id
        )

    async def stop(self, id: int) -> None:
        """
        Stop a running task.

        Args:
            id: The ID of the task.
        """

        # INVOKE <id> Task.Stop
        # -> R:INVOKE <id> <rcode> Task.Stop
        await self.command_client.command("INVOKE", id, "Task.Stop")
