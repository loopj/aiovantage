from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base, xml_attr, xml_tag

if TYPE_CHECKING:
    from .area import Area
    from .station import Station


@dataclass
class DryContact(Base):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    area_id: Optional[int] = xml_tag("Area")
    station_id: Optional[int] = xml_tag("Parent")

    @property
    def area(self) -> Optional["Area"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.get(id=self.area_id)

    @property
    def station(self) -> Optional["Station"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.stations.get(id=self.station_id)