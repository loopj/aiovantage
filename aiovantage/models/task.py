from collections.abc import Sequence
from dataclasses import dataclass

from typing_extensions import override

from aiovantage.hc_client import StatusType
from aiovantage.models.system_object import SystemObject


@dataclass
class Task(SystemObject):
    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:TASK {vid} {state}
        self._logger.debug(f"Task triggered for {self.name} ({self.id}) to {args}")
