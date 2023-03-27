from typing import Any

from ..models.load import Load
from .base import BaseController


class LoadsController(BaseController[Load]):
    item_type = Load
    vantage_types = ["Load"]
    event_types = ["LOAD"]

    # S:LOAD {vid} {level}
    def handle_event(self, obj: Load, args: Any) -> None:
        level = float(args[0])
        obj._level = level

        self._logger.debug(f"Load level changed for {obj.name} ({obj.id}) to {level}")
