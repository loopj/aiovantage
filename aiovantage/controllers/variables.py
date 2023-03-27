import xml.etree.ElementTree as ET
from typing import Any

from ..models.variable import Variable
from ..utils import get_element_text
from .base import BaseController


class VariablesController(BaseController[Variable]):
    item_cls = Variable
    vantage_types = ["GMem"]
    event_types = ["VARIABLE"]

    def from_xml(cls, el: ET.Element) -> "Variable":
        return Variable(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
        )

    # TODO
    def handle_event(self, obj: Variable, args: Any) -> None:
        self._logger.debug(f"Variable updated {obj.name} ({obj.id})")
