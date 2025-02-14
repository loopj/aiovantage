from aiovantage.objects import Task

from .base import Controller


class TasksController(Controller[Task]):
    """Tasks controller."""

    vantage_types = ("Task",)
