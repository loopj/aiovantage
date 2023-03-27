import xml.etree.ElementTree as ET

from ..models.station import Station
from ..utils import get_element_int, get_element_text
from .base import BaseController


class StationsController(BaseController[Station]):
    item_cls = Station
    vantage_types = (
        "Keypad",
        "Dimmer",
        "ScenePointRelay",
        "DualRelayStation",
        "EqCtrl",
        "EqUX",
    )

    def from_xml(cls, el: ET.Element) -> "Station":
        return Station(
            id=int(el.attrib["VID"]),
            name=get_element_text(el, "Name"),
            display_name=get_element_text(el, "DName"),
            area_id=get_element_int(el, "Area"),
            bus_id=get_element_int(el, "Bus"),
        )
