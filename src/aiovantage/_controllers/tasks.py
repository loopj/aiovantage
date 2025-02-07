from aiovantage.controllers import BaseController
from aiovantage.objects import Task


class TasksController(BaseController[Task]):
    """Tasks controller."""

    vantage_types = ("Task",)
