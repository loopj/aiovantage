from typing import Any

from ..models.task import Task
from .base import BaseController


class TasksController(BaseController[Task]):
    item_type = Task
    vantage_types = ["Task"]
    event_types = ["TASK"]

    # S:TASK {vid} {state}
    def handle_event(self, obj: Task, args: Any) -> None:
        state = int(args[0])
        self._logger.debug(f"Task triggered {obj.name} ({obj.id}) to {state}")
