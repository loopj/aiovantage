from enum import IntEnum

from typing_extensions import override

from .base import Interface, method


class TaskInterface(Interface):
    """Task interface."""

    interface_name = "Task"

    class Status(IntEnum):
        """Task status."""

        NotReady = 0
        Ready = 1
        Compiling = 2
        OutOfSync = 3
        Invalid = 4

    # Properties
    state: int | None = None
    running: bool | None = None
    context_state: bool | None = None

    # Methods
    @method("Start")
    async def start(self) -> None:
        """Start a task."""
        # TODO: Add support for Task.Start parameters
        # INVOKE <id> Task.Start <source> <event> <param1> <param2>
        # -> R:INVOKE <id> <rcode (0/1)> Task.Start <source> <event> <param1> <param2>
        await self.invoke("Task.Start")

    @method("Stop")
    async def stop(self) -> None:
        """Stop a running task."""
        # INVOKE <id> Task.Stop
        # -> R:INVOKE <id> <rcode> Task.Stop
        await self.invoke("Task.Stop")

    @method("Cancel")
    async def cancel(self) -> None:
        """Cancel a scheduled task."""
        # INVOKE <id> Task.Cancel
        # -> R:INVOKE <id> <rcode> Task.Cancel
        await self.invoke("Task.Cancel")

    @method("IsRunning", property="running")
    async def is_running(self) -> bool:
        """Get the running state of a task."""
        # INVOKE <id> Task.IsRunning
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        return await self.invoke("Task.IsRunning")

    @method("GetState", property="state")
    async def get_state(self) -> int:
        """Get the state of a task.

        Returns:
            The LED state of the task.
        """
        # INVOKE <id> Task.GetState
        # -> R:INVOKE <id> <state> Task.GetState
        return await self.invoke("Task.GetState")

    @method("SetState")
    async def set_state(self, state: int) -> None:
        """Set the state of a task.

        Args:
            state: The state to set the task to.
        """
        # INVOKE <id> Task.SetState <state>
        # -> R:INVOKE <id> <rcode> Task.SetState <state>
        await self.invoke("Task.SetState", state)

    @method("GetStatus")
    async def get_status(self) -> Status:
        """Get the status of a task.

        Returns:
            The status of the task.
        """
        # INVOKE <id> Task.GetStatus
        # -> R:INVOKE <id> <status> Task.GetStatus
        return await self.invoke("Task.GetStatus")

    @method("GetContextState")
    async def get_context_state(self) -> int:
        """Get the context-aware task state.

        Returns:
            The context aware state of the task.
        """
        # INVOKE <id> Task.GetContextState
        # -> R:INVOKE <id> <context state> Task.GetContextState
        return await self.invoke("Task.GetContextState")

    @method("HasContextState", property="context_state")
    async def has_context_state(self) -> bool:
        """Check if the task is context-aware.

        Returns:
            True if the task is context-aware, False otherwise.
        """
        # INVOKE <id> Task.HasContextState
        # -> R:INVOKE <id> <has context state (0/1)> Task.HasContextState
        return await self.invoke("Task.HasContextState")

    @override
    def handle_category_status(self, category: str, *args: str) -> list[str]:
        if category == "TASK":
            # STATUS TASK
            # -> S:TASK <id> <state>
            return self.update_properties({"state": int(args[0])})

        return super().handle_category_status(category, *args)
