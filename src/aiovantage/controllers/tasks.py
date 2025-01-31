"""Controller holding and managing Vantage tasks."""

from aiovantage.objects import Task

from .base import BaseController


class TasksController(BaseController[Task]):
    """Controller holding and managing Vantage tasks."""

    vantage_types = ("Task",)
