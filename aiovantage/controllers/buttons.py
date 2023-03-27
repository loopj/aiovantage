import xml.etree.ElementTree as ET
from typing import Any

from ..models.button import Button
from ..utils import get_element_int, get_element_text
from .base import BaseController


class ButtonsController(BaseController[Button]):
    item_cls = Button
    vantage_types = ["Button"]
    event_types = ["BTN"]

    def from_xml(cls, el: ET.Element) -> "Button":
        return Button(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
            station_id=get_element_int(el, "Parent"),
            text=get_element_text(el, "Text1"),
        )

    # S:BTN {vid} {PRESS|RELEASE}
    def handle_event(self, obj: Button, args: Any) -> None:
        state = args[0]

        self._logger.debug(
            f"Button state changed for {obj.name} {obj.text} ({obj.id}) to {state}"
        )
