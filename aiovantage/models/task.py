from collections.abc import Sequence
from dataclasses import dataclass

from typing_extensions import override

from ..clients.hc import StatusType
from .system_object import SystemObject
from ..xml_dataclass import attr_field, element_field


@dataclass
class Task(SystemObject):
    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:TASK {vid} {state}
        self._logger.debug(
            f"Task triggered for {self.name} ({self.id}) to {args}"
        )