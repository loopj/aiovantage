from typing import Any

from ..models.omni_sensor import OmniSensor
from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    item_cls = OmniSensor
    vantage_types = ["OmniSensor"]
    event_types = ["TEMP", "POWER", "CURRENT"]

    # S:TEMP {vid} {level}
    # S:POWER {vid} {level}
    # S:CURRENT {vid} {level}
    def handle_event(self, obj: OmniSensor, args: Any) -> None:
        level = float(args[0])
        obj._level = level

        self._logger.debug(
            f"OmniSensor level changed for {obj.name} ({obj.id}) to {level}"
        )
