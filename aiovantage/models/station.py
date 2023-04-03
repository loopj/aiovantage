from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from aiovantage.models.location_object import LocationObject
from aiovantage.query import QuerySet
from aiovantage.xml_dataclass import element_field

if TYPE_CHECKING:
    from aiovantage.models.button import Button
    from aiovantage.models.dry_contact import DryContact


@dataclass
class Station(LocationObject):
    bus_id: Optional[int] = element_field(name="Bus", default=None)

    @property
    def buttons(self) -> QuerySet["Button"]:
        return self.vantage.buttons.filter(station_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self.vantage.dry_contacts.filter(station_id=self.id)
