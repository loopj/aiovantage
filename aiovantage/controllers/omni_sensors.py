import xml.etree.ElementTree as ET
from typing import Any

from ..models.omni_sensor import OmniSensor
from ..utils import get_element_text
from .base import BaseController


class OmniSensorsController(BaseController[OmniSensor]):
    item_cls = OmniSensor
    vantage_types = ["OmniSensor"]
    event_types = ["TEMP", "POWER", "CURRENT"]

    def from_xml(self, el: ET.Element) -> "OmniSensor":
        return OmniSensor(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
        )

    # S:TEMP {vid} {level}
    # S:POWER {vid} {level}
    # S:CURRENT {vid} {level}
    def handle_event(self, obj: OmniSensor, args: Any) -> None:
        level = float(args[0])
        obj._level = level

        self._logger.debug(
            f"OmniSensor level changed for {obj.name} ({obj.id}) to {level}"
        )
