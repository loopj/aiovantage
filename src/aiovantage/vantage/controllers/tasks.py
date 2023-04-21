from aiovantage.aci_client.system_objects import Task
from aiovantage.vantage.controllers.base import BaseController

# TASK <task vid> <eventType>
#   -> R:TASK <task vid> <eventType>

# GETTASK <task vid>
#   -> R:GETTASK <task vid> <0/1>

# STATUS TASK
#   -> R:STATUS TASK
#   -> S:TASK <task vid> <0/1>

# ADDSTATUS <task vid>
#   -> R:ADDSTATUS <task vid>
#   -> S:STATUS <task vid> Task.GetState <0/1>
#   -> S:STATUS <task vid> Task.IsRunning <0/1>


class TasksController(BaseController[Task]):
    item_cls = Task
    vantage_types = (Task,)
    status_types = ("TASK",)
