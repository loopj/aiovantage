import xml.etree.ElementTree as ET
from typing import Any

from ..models.load import Load
from ..utils import get_element_int, get_element_text
from .base import BaseController


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ["Load"]
    event_types = ["LOAD"]

    def from_xml(self, el: ET.Element) -> "Load":
        return Load(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
            load_type=get_element_text(el, "LoadType"),
            area_id=get_element_int(el, "Area"),
        )

    # S:LOAD {vid} {level}
    def handle_event(self, obj: Load, args: Any) -> None:
        level = float(args[0])
        obj._level = level

        self._logger.debug(f"Load level changed for {obj.name} ({obj.id}) to {level}")
