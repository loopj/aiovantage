from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..query import QuerySet
from .base import Base

if TYPE_CHECKING:
    from .area import Area
    from .button import Button
    from .dry_contact import DryContact


@dataclass
class Station(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    area_id: Optional[int] = None
    bus_id: Optional[int] = None

    @property
    def area(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.area_id)

    @property
    def buttons(self) -> QuerySet["Button"]:
        return self._vantage.buttons.filter(station_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self._vantage.dry_contacts.filter(station_id=self.id)
