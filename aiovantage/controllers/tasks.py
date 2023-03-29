from ..clients.hc import StatusType
from ..models.task import Task
from .base import BaseController


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = ("Task",)
    status_types = (StatusType.TASK,)