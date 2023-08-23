"""Interface for querying and controlling tasks."""

from typing import Sequence

from .base import Interface


class TaskInterface(Interface):
    """Interface for querying and controlling tasks."""

    async def start(self, vid: int) -> None:
        """Start a task.

        Args:
            vid: The Vantage ID of the task.
        """
        # INVOKE <id> Task.Start <source> <event> <param1> <param2>
        # -> R:INVOKE <id> <rcode (0/1)> Task.Start <source> <event> <param1> <param2>
        await self.invoke(vid, "Task.Start")

    async def stop(self, vid: int) -> None:
        """Stop a running task.

        Args:
            vid: The Vantage ID of the task.
        """
        # INVOKE <id> Task.Stop
        # -> R:INVOKE <id> <rcode> Task.Stop
        await self.invoke(vid, "Task.Stop")

    async def is_running(self, vid: int) -> bool:
        """Get the running state of a task.

        Args:
            vid: The Vantage ID of the task.
        """
        # INVOKE <id> Task.IsRunning
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        response = await self.invoke(vid, "Task.IsRunning")
        is_running = bool(int(response.args[1]))

        return is_running

    async def get_state(self, vid: int) -> int:
        """Get the LED state of a task.

        Args:
            vid: The Vantage ID of the task.
        """
        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state> Task.GetState
        response = await self.invoke(vid, "Task.GetState")
        task_state = int(response.args[1])

        return task_state

    @classmethod
    def parse_get_state_status(cls, args: Sequence[str]) -> int:
        """Parse a 'Task.GetState' event.

        Args:
            args: The arguments of the event.

        Returns:
            The LED state of the task.
        """
        # ELLOG STATUS ON
        # -> EL: <id> Task.GetState <state (0/1)>
        # STATUS ADD <id>
        # -> S:STATUS <id> Task.GetState <state (0/1)>
        return int(args[0])

    @classmethod
    def parse_is_running_status(cls, args: Sequence[str]) -> bool:
        """Parse a 'Task.IsRunning' event.

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
