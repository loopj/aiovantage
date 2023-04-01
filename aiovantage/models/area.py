from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..query import QuerySet
from .location_object import LocationObject

if TYPE_CHECKING:
    from .dry_contact import DryContact
    from .load import Load
    from .station import Station


@dataclass
class Area(LocationObject):
    @property
    def areas(self) -> QuerySet["Area"]:
        return self.vantage.areas.filter(area_id=self.id)

    @property
    def stations(self) -> QuerySet["Station"]:
        return self.vantage.stations.filter(area_id=self.id)

    @property
    def loads(self) -> QuerySet["Load"]:
        return self.vantage.loads.filter(area_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self.vantage.dry_contacts.filter(area_id=self.id)
