"""Tasks controller."""

from aiovantage.objects import Task

from .base import BaseController


class TasksController(BaseController[Task]):
    """Tasks controller."""

    vantage_types = ("Task",)
