from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..query import QuerySet
from .vantage_object import VantageObject
from .xml_model import xml_attr, xml_tag

if TYPE_CHECKING:
    from .area import Area
    from .button import Button
    from .dry_contact import DryContact


@dataclass
class Station(VantageObject):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name", default=None)
    display_name: Optional[str] = xml_tag("DName", default=None)
    area_id: Optional[int] = xml_tag("Area", default=None)
    bus_id: Optional[int] = xml_tag("Bus", default=None)

    @property
    def area(self) -> Optional["Area"]:
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
