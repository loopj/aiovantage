from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..query import QuerySet
from .vantage_object import VantageObject
from .xml_model import attr, element

if TYPE_CHECKING:
    from .area import Area
    from .button import Button
    from .dry_contact import DryContact


@dataclass
class Station(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)
    area_id: int | None = element(alias="Area", default=None)
    bus_id: int | None = element(alias="Bus", default=None)

    @property
    def area(self) -> "Area | None":
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.get(id=self.area_id)

    @property
    def buttons(self) -> QuerySet["Button"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.buttons.filter(station_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.dry_contacts.filter(station_id=self.id)
