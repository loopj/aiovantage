from ..models.task import Task
from .base import BaseController


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = ["Task"]
    event_types = ["TASK"]