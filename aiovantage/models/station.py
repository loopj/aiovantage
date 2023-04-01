from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..query import QuerySet
from .location_object import LocationObject
from ..xml_dataclass import element_field

if TYPE_CHECKING:
    from .button import Button
    from .dry_contact import DryContact


@dataclass
class Station(LocationObject):
    bus_id: int | None = element_field(name="Bus", default=None)

    @property
    def buttons(self) -> QuerySet["Button"]:
        return self.vantage.buttons.filter(station_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self.vantage.dry_contacts.filter(station_id=self.id)
