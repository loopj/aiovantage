import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..query import QuerySet
from .base import Base
from .utils import get_element_int

if TYPE_CHECKING:
    from .area import Area
    from .button import Button
    from .dry_contact import DryContact


@dataclass
class Station(Base):
    area_id: Optional[int] = None
    bus_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el: ET.Element) -> "Station":
        obj = super().from_xml(el)
        obj.area_id = get_element_int(el, "Area")
        obj.bus_id = get_element_int(el, "Bus")
        return obj

    @property
    def area(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.area_id)

    @property
    def buttons(self) -> QuerySet["Button"]:
        return self._vantage.buttons.filter(station_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self._vantage.dry_contacts.filter(station_id=self.id)
