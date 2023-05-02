from typing import Sequence

from typing_extensions import override

from aiovantage.config_client.objects import Task
from aiovantage.vantage.controllers.base import StatefulController

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


class TasksController(StatefulController[Task]):
    item_cls = Task
    vantage_types = (Task,)

    @override
    async def fetch_initial_state(self, id: int) -> None:
        ...

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        ...
