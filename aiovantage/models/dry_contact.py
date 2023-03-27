import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base
from .utils import get_element_int

if TYPE_CHECKING:
    from .area import Area
    from .station import Station


@dataclass
class DryContact(Base):
    area_id: Optional[int] = None
    station_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el: ET.Element) -> "DryContact":
        obj = super().from_xml(el)
        obj.station_id = get_element_int(el, "Parent")
        obj.area_id = get_element_int(el, "Area")
        return obj

    @property
    def area(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.area_id)

    @property
    def station(self) -> Optional["Station"]:
        return self._vantage.stations.get(id=self.station_id)
