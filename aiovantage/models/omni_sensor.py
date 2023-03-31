from collections.abc import Sequence
from dataclasses import dataclass

from typing_extensions import override

from ..clients.hc import StatusType
from .vantage_object import VantageObject
from .xml_model import attr, element


@dataclass
class OmniSensor(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)
    _level: float | None = None

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:TEMP {vid} {level}
        # S:POWER {vid} {level}
        # S:CURRENT {vid} {level}
        level = float(args[0])
        self._level = level

        self._logger.debug(
            f"OmniSensor level changed for {self.name} ({self.id}) to {level}"
        )