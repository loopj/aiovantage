import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base
from .utils import get_element_int, get_element_text

if TYPE_CHECKING:
    from .station import Station


@dataclass
class Button(Base):
    text: Optional[str] = None
    station_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el: ET.Element) -> "Button":
        obj = super().from_xml(el)
        obj.station_id = get_element_int(el, "Parent")
        obj.text = get_element_text(el, "Text1")
        return obj

    @property
    def station(self) -> Optional["Station"]:
        return self._vantage.stations.get(id=self.station_id)
