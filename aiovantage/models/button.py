from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base, xml_attr, xml_tag

if TYPE_CHECKING:
    from .station import Station


@dataclass
class Button(Base):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    text: Optional[str] = xml_tag("Text1")
    station_id: Optional[int] = xml_tag("Parent")

    @property
    def station(self) -> Optional["Station"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.stations.get(id=self.station_id)