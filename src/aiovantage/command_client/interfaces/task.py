from typing import Sequence

from .base import Interface


class TaskInterface(Interface):
    async def is_running(self, id: int) -> bool:
        """
        Get the running state of a task.

        Args:
            id: The ID of the task.
        """

        # INVOKE <id> Task.IsRunning
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        response = await self.invoke(id, "Task.IsRunning")
        is_running = bool(int(response.args[1]))

        return is_running

    async def get_state(self, id: int) -> bool:
        """
        Get the state of a task.

        Args:
            id: The ID of the task.
        """

        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state (0/1)> Task.GetState
        response = await self.invoke(id, "Task.GetState")
        task_state = bool(int(response.args[1]))

        return task_state

    async def start(self, id: int) -> None:
        """
        Start a task.

        Args:
            id: The ID of the task.
        """

        # INVOKE <id> Task.Start <source> <event> <param1> <param2>
        # -> R:INVOKE <id> <rcode (0/1)> Task.Start <source> <event> <param1> <param2>
        await self.invoke(id, "Task.Start")

    async def stop(self, id: int) -> None:
        """
        Stop a running task.

        Args:
            id: The ID of the task.
        """

        # INVOKE <id> Task.Stop
        # -> R:INVOKE <id> <rcode> Task.Stop
        await self.invoke(id, "Task.Stop")

    @classmethod
    def parse_task_status(cls, args: Sequence[str]) -> bool:
        """
        Parse a simple "S:TASK" event.

        Args:
            args: The arguments of the event.

        Returns:
            The state of the task.
        """

        # STATUS TASK
        # -> S:TASK <id> <state (0/1)>
        return bool(int(args[0]))

    @classmethod
    def parse_get_state_status(cls, args: Sequence[str]) -> bool:
        """
        Parse a "Task.GetState" event.

        Args:
            args: The arguments of the event.

        Returns:
            The state of the task.
        """

        # ELLOG STATUS ON
        # -> EL: <id> Task.GetState <state (0/1)>

        # STATUS ADD <id>
        # -> S:STATUS <id> Task.GetState <state (0/1)>
        return bool(int(args[0]))

    @classmethod
    def parse_is_running_status(cls, args: Sequence[str]) -> bool:
        """
        Parse a "Task.IsRunning" event.

        Args:
            args: The arguments of the event.

        Returns:
            The running state of the task.
        """

        # ELLOG STATUS ON
        # -> EL: <id> Task.IsRunning <running (0/1)>

        # STATUS ADD <id>
        # -> S:STATUS <id> Task.IsRunning <running (0/1)>
        return bool(int(args[0]))
