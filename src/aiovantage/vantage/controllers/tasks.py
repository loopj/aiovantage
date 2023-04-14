from aiovantage.aci_client.system_objects import Task
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController

# TASK <task vid> <eventType (PRESS/RELEASE/HOLD/TIMER/DATA/POSITION/INRANGE/OUTOFRANGE/TEMPERATURE/DAYMODE/FANMODE/OPERATIONMODE/CONNECT/DISCONNECT/BOOT/LEARN/CANCEL/NONE)>
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
    vantage_types = ("Task",)
    status_types = (StatusType.TASK,)
