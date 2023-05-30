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
            event_type: The type event to send to the task, defaults to RELEASE.
            source_id: The object ID of the source sending the event, defaults to 0.
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
