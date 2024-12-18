"""Interface for querying and controlling tasks."""

from .base import Interface


class TaskInterface(Interface):
    """Interface for querying and controlling tasks."""

    method_signatures = {
        "Task.IsRunning": bool,
        "Task.GetState": int,
    }

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
        return await self.invoke(vid, "Task.IsRunning", as_type=bool)

    async def get_state(self, vid: int) -> int:
        """Get the state of a task.

        Args:
            vid: The Vantage ID of the task.

        Returns:
            The LED state of the task.
        """
        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state> Task.GetState
        return await self.invoke(vid, "Task.GetState", as_type=int)

    async def set_state(self, vid: int, state: int) -> None:
        """Set the state of a task.

        Args:
            vid: The Vantage ID of the task.
            state: The state to set the task to.
        """
        # INVOKE <id> Task.SetState <state>
        # -> R:INVOKE <id> <rcode> Task.SetState <state>
        await self.invoke(vid, "Task.SetState", state)
