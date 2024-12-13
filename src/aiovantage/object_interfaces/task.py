"""Interface for querying and controlling tasks."""

from aiovantage.object_interfaces.base import Interface


class TaskInterface(Interface):
    """Interface for querying and controlling tasks."""

    method_signatures = {
        "Task.IsRunning": bool,
        "Task.GetState": int,
    }

    state: int
    running: bool

    async def start(self) -> None:
        """Start a task."""
        # INVOKE <id> Task.Start <source> <event> <param1> <param2>
        # -> R:INVOKE <id> <rcode (0/1)> Task.Start <source> <event> <param1> <param2>
        await self.invoke("Task.Start")

    async def stop(self) -> None:
        """Stop a running task."""
        # INVOKE <id> Task.Stop
        # -> R:INVOKE <id> <rcode> Task.Stop
        await self.invoke("Task.Stop")

    async def cancel(self) -> None:
        """Cancel a scheduled task."""
        # INVOKE <id> Task.Cancel
        # -> R:INVOKE <id> <rcode> Task.Cancel
        await self.invoke("Task.Cancel")

    async def is_running(self) -> bool:
        """Get the running state of a task."""
        # INVOKE <id> Task.IsRunning
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        return await self.invoke("Task.IsRunning", as_type=bool)

    async def get_state(self) -> int:
        """Get the state of a task.

        Returns:
            The LED state of the task.
        """
        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state> Task.GetState
        return await self.invoke("Task.GetState", as_type=int)

    async def set_state(self, state: int) -> None:
        """Set the state of a task.

        Args:
            vid: The Vantage ID of the task.
            state: The state to set the task to.
        """
        # INVOKE <id> Task.SetState <state>
        # -> R:INVOKE <id> <rcode> Task.SetState <state>
        await self.invoke("Task.SetState", state)
