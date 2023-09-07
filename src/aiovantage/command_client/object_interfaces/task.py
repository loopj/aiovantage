"""Interface for querying and controlling tasks."""

from .base import Interface, InterfaceResponse, bool_result, int_result


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
        response = await self.invoke(vid, "Task.IsRunning")
        return self.parse_is_running_response(response)

    async def get_state(self, vid: int) -> int:
        """Get the state of a task.

        Args:
            vid: The Vantage ID of the task.

        Returns:
            The LED state of the task.
        """
        # INVOKE <id> Task.GetState
        response = await self.invoke(vid, "Task.GetState")
        return self.parse_get_state_response(response)

    async def set_state(self, vid: int, state: int) -> None:
        """Set the state of a task.

        Args:
            vid: The Vantage ID of the task.
            state: The state to set the task to.
        """
        # INVOKE <id> Task.SetState <state>
        # -> R:INVOKE <id> <rcode> Task.SetState <state>
        await self.invoke(vid, "Task.SetState", state)

    @classmethod
    def parse_is_running_response(cls, response: InterfaceResponse) -> bool:
        """Parse a 'Task.IsRunning' response."""
        # -> R:INVOKE <id> <running (0/1)> Task.IsRunning
        # -> S:STATUS <id> Task.IsRunning <running (0/1)>
        # -> EL: <id> Task.IsRunning <running (0/1)>
        return bool_result(response)

    @classmethod
    def parse_get_state_response(cls, response: InterfaceResponse) -> int:
        """Parse a 'Task.GetState' response."""
        # -> R:INVOKE <id> <state> Task.GetState
        # -> S:STATUS <id> Task.GetState <state>
        # -> EL: <id> Task.GetState <state>
        return int_result(response)
