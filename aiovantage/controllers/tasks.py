from aiovantage.hc_client import StatusType
from aiovantage.controllers.base import BaseController
from aiovantage.models.task import Task


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = ("Task",)
    status_types = (StatusType.TASK,)
