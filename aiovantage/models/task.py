from dataclasses import dataclass
from typing import Any, Optional

from .vantage_object import VantageObject
from .xml_model import xml_attr, xml_tag


@dataclass
class Task(VantageObject):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name", default=None)
    display_name: Optional[str] = xml_tag("DName", default=None)

    # S:TASK {vid} {state}
    def status_handler(self, args: Any) -> None:
        self._logger.debug(
            f"Task triggered for {self.name} ({self.id}) to {args}"
        )