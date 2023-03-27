from typing import Any

from ..models.variable import Variable
from .base import BaseController


class VariablesController(BaseController[Variable]):
    item_type = Variable
    vantage_types = ["GMem"]
    event_types = ["VARIABLE"]

    # TODO
    def handle_event(self, obj: Variable, args: Any) -> None:
        self._logger.debug(f"Variable updated {obj.name} ({obj.id})")
