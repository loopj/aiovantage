import xml.etree.ElementTree as ET

from ..models.area import Area
from ..utils import get_element_int, get_element_text
from .base import BaseController


class AreasController(BaseController[Area]):
    item_cls = Area
    vantage_types = ["Area"]

    def from_xml(cls, el: ET.Element) -> "Area":
        return Area(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
            parent_id=get_element_int(el, "Area"),
        )
