from aiovantage.aci_client.system_objects import Task
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = ("Task",)
    status_types = (StatusType.TASK,)
