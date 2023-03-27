import xml.etree.ElementTree as ET
from typing import Any

from ..models.dry_contact import DryContact
from ..utils import get_element_int, get_element_text
from .base import BaseController


class DryContactsController(BaseController[DryContact]):
    item_cls = DryContact
    vantage_types = ["DryContact"]
    event_types = ["BTN"]

    def from_xml(cls, el: ET.Element) -> "DryContact":
        return DryContact(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
            station_id = get_element_int(el, "Parent"),
            area_id = get_element_int(el, "Area"),
        )

    # S:BTN {vid} {PRESS|RELEASE}
    def handle_event(self, obj: DryContact, args: Any) -> None:
        state = args[0]

        self._logger.debug(
            f"DryContact state changed for {obj.name} ({obj.id}) to {state}"
        )
