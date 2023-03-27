from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..query import QuerySet
from .base import Base

if TYPE_CHECKING:
    from .dry_contact import DryContact
    from .load import Load
    from .station import Station


@dataclass
class Area(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    parent_id: Optional[int] = None

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
