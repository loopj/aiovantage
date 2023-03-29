from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..query import QuerySet
from .base import Base, xml_attr, xml_tag

if TYPE_CHECKING:
    from .dry_contact import DryContact
    from .load import Load
    from .station import Station


@dataclass
class Area(Base):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    parent_id: Optional[int] = xml_tag("Area")

    @property
    def parent(self) -> Optional["Area"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.get(id=self.parent_id)

    @property
    def areas(self) -> QuerySet["Area"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.filter(parent_id=self.id)

    @property
    def stations(self) -> QuerySet["Station"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.stations.filter(area_id=self.id)

    @property
    def loads(self) -> QuerySet["Load"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.loads.filter(area_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.dry_contacts.filter(area_id=self.id)
