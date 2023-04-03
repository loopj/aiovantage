from dataclasses import dataclass
from typing import TYPE_CHECKING

from aiovantage.models.location_object import LocationObject
from aiovantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage.models.dry_contact import DryContact
    from aiovantage.models.load import Load
    from aiovantage.models.station import Station


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
