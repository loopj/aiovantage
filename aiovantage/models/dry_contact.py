import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base
from ..utils import get_element_int

if TYPE_CHECKING:
    from .area import Area
    from .station import Station


@dataclass
class DryContact(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    area_id: Optional[int] = None
    station_id: Optional[int] = None

    @property
    def area(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.area_id)

    @property
    def station(self) -> Optional["Station"]:
        return self._vantage.stations.get(id=self.station_id)
