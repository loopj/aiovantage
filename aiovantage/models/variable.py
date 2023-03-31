from collections.abc import Sequence
from dataclasses import dataclass

from typing_extensions import override

from ..clients.hc import StatusType
from .vantage_object import VantageObject
from .xml_model import attr, element


@dataclass
class Variable(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # TODO: STATUS ? ?
        self._logger.debug(f"Variable updated {self.name} ({self.id}) to ({args})")
