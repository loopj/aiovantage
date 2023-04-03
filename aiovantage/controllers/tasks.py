from aiovantage.clients.hc import StatusType
from aiovantage.models.task import Task
from aiovantage.controllers.base import BaseController


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = ("Task",)
    status_types = (StatusType.TASK,)
