from dataclasses import dataclass

from .vantage_object import VantageObject
from .xml_model import attr, element


@dataclass
class Task(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)

    # S:TASK {vid} {state}
    def status_handler(self, args: list[str]) -> None:
        self._logger.debug(
            f"Task triggered for {self.name} ({self.id}) to {args}"
        )