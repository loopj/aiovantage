from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..query import QuerySet
from .vantage_object import VantageObject
from .xml_model import attr, element

if TYPE_CHECKING:
    from .dry_contact import DryContact
    from .load import Load
    from .station import Station


@dataclass
class Area(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)
    parent_id: int | None = element(alias="Area", default=None)

    @property
    def parent(self) -> "Area | None":
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
