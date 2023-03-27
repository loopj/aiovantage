import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..query import QuerySet
from .base import Base
from .utils import get_element_int

if TYPE_CHECKING:
    from .dry_contact import DryContact
    from .load import Load
    from .station import Station


@dataclass
class Area(Base):
    parent_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el: ET.Element) -> "Area":
        obj = super().from_xml(el)
        obj.parent_id = get_element_int(el, "Area")
        return obj

    @property
    def parent(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.parent_id)

    @property
    def areas(self) -> QuerySet["Area"]:
        return self._vantage.areas.filter(parent_id=self.id)

    @property
    def stations(self) -> QuerySet["Station"]:
        return self._vantage.stations.filter(area_id=self.id)

    @property
    def loads(self) -> QuerySet["Load"]:
        return self._vantage.loads.filter(area_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self._vantage.dry_contacts.filter(area_id=self.id)
