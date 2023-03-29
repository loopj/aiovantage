from dataclasses import dataclass
from typing import Any, Optional

from .vantage_object import VantageObject
from .xml_model import xml_attr, xml_tag


@dataclass
class OmniSensor(VantageObject):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    _level: Optional[float] = None

    # S:TEMP {vid} {level}
    # S:POWER {vid} {level}
    # S:CURRENT {vid} {level}
    def status_handler(self, args: Any) -> None:
        level = float(args[0])
        self._level = level

        self._logger.debug(
            f"OmniSensor level changed for {self.name} ({self.id}) to {level}"
        )