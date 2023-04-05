from collections.abc import Sequence
from dataclasses import dataclass

from typing_extensions import override

from aiovantage.hc_client import StatusType
from aiovantage.models.system_object import SystemObject


@dataclass
class Variable(SystemObject):
    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # TODO: STATUS ? ?
        self._logger.debug(f"Variable updated {self.name} ({self.id}) to ({args})")
