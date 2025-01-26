"""Interface for querying and controlling tasks."""

from enum import IntEnum

from .base import Interface


class TaskInterface(Interface):
    """Interface for querying and controlling tasks."""

    class Status(IntEnum):
        """Task status."""

        NotReady = 0
        Ready = 1
        Compiling = 2
        OutOfSync = 3
        Invalid = 4

    method_signatures = {
        "Task.IsRunning": bool,
        "Task.GetState": int,
        "Task.GetStatus": Status,
        "Task.GetContextState": int,
        "Task.HasContextState": bool,
    }

    async def start(self, vid: int) -> None:
        """Start a task.

        Args:
            vid: The Vantage ID of the task.
        """
        # TODO: Add support for Task.Start parameters
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

    async def cancel(self, vid: int) -> None:
        """Cancel a scheduled task.

        Args:
            vid: The Vantage ID of the task.
        """
        # INVOKE <id> Task.Cancel
        # -> R:INVOKE <id> <rcode> Task.Cancel
        await self.invoke(vid, "Task.Cancel")

    async def is_running(self, vid: int) -> bool:
        """Get the running state of a task.

        Args:
            vid: The Vantage ID of the task.
        """
        # INVOKE <id> Task.IsRunning
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        return await self.invoke(vid, "Task.IsRunning")

    async def get_state(self, vid: int) -> int:
        """Get the state of a task.

        Args:
            vid: The Vantage ID of the task.

        Returns:
            The LED state of the task.
        """
        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state> Task.GetState
        return await self.invoke(vid, "Task.GetState")

    async def set_state(self, vid: int, state: int) -> None:
        """Set the state of a task.

        Args:
            vid: The Vantage ID of the task.
            state: The state to set the task to.
        """
        # INVOKE <id> Task.SetState <state>
        # -> R:INVOKE <id> <rcode> Task.SetState <state>
        await self.invoke(vid, "Task.SetState", state)

    async def get_status(self, vid: int) -> Status:
        """Get the status of a task.

        Args:
            vid: The Vantage ID of the task.

        Returns:
            The status of the task.
        """
        # INVOKE <id> Task.GetStatus
        # -> R:INVOKE <id> <status> Task.GetStatus
        return await self.invoke(vid, "Task.GetStatus")

    async def get_context_state(self, vid: int) -> int:
        """Get the context-aware task state.

        Args:
            vid: The Vantage ID of the task.

        Returns:
            The context aware state of the task.
        """
        # INVOKE <id> Task.GetContextState
        # -> R:INVOKE <id> <context state> Task.GetContextState
        return await self.invoke(vid, "Task.GetContextState")

    async def has_context_state(self, vid: int) -> bool:
        """Check if the task is context-aware.

        Args:
            vid: The Vantage ID of the task.

        Returns:
            True if the task is context-aware, False otherwise.
        """
        # INVOKE <id> Task.HasContextState
        # -> R:INVOKE <id> <has context state (0/1)> Task.HasContextState
        return await self.invoke(vid, "Task.HasContextState")
