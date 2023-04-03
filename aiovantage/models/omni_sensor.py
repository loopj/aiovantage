from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Optional

from typing_extensions import override

from ..clients.hc import StatusType
from .system_object import SystemObject


@dataclass
class OmniSensor(SystemObject):
    def __post_init__(self) -> None:
        self._level: Optional[float] = None

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
